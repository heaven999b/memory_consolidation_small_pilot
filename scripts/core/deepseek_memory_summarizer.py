from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


class DeepSeekMemorySummarizer:
    def __init__(
        self,
        cache_dir: Path,
        timeout_s: int = 180,
        max_retries: int = 2,
        run_cwd: Path | None = None,
        log_path: Path | None = None,
        verbose: bool | None = None,
        backend: str | None = None,
    ) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self.run_cwd = run_cwd or Path("/private/tmp")
        self.run_cwd.mkdir(parents=True, exist_ok=True)
        self.log_path = log_path or (self.cache_dir.parent / f"{self.cache_dir.name}_summarizer_log.jsonl")
        self.verbose = (os.environ.get("DEEPSEEK_SUMMARIZER_VERBOSE", "").strip() not in {"", "0", "false", "False"}) if verbose is None else verbose
        self.backend = (backend or os.environ.get("MEMORY_SUMMARIZER_BACKEND", "deepseek_cli")).strip().lower()

    def _log_event(self, payload: dict[str, Any]) -> None:
        event = dict(payload)
        event["timestamp"] = round(time.time(), 3)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        if self.verbose:
            printable = {key: event[key] for key in ("event", "cache_key", "attempt", "status", "duration_s", "message") if key in event}
            print(f"[deepseek] {json.dumps(printable, ensure_ascii=False)}", flush=True)

    def summarize(
        self,
        *,
        cache_key: str,
        prompt: str,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        cache_path = self.cache_dir / f"{cache_key}.json"
        if cache_path.exists():
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            cached["cache_hit"] = True
            cached["cache_path"] = str(cache_path)
            self._log_event(
                {
                    "event": "cache_hit",
                    "cache_key": cache_key,
                    "status": "ok",
                    "message": str(cache_path),
                }
            )
            return cached

        last_error: str | None = None
        for attempt in range(self.max_retries + 1):
            t0 = time.time()
            self._log_event(
                {
                    "event": "attempt_start",
                    "cache_key": cache_key,
                    "attempt": attempt + 1,
                    "status": "running",
                    "message": f"timeout={self.timeout_s}s",
                }
            )
            try:
                payload = self._run_backend(prompt=prompt, schema=schema)
            except subprocess.TimeoutExpired as exc:
                duration_s = round(time.time() - t0, 3)
                last_error = f"timeout after {self.timeout_s}s"
                self._log_event(
                    {
                        "event": "attempt_timeout",
                        "cache_key": cache_key,
                        "attempt": attempt + 1,
                        "status": "timeout",
                        "duration_s": duration_s,
                        "message": (exc.stderr or exc.stdout or last_error or "")[:400],
                    }
                )
                if attempt >= self.max_retries:
                    break
                time.sleep(1.5 * (attempt + 1))
                continue
            except TimeoutError as exc:
                duration_s = round(time.time() - t0, 3)
                last_error = str(exc)
                self._log_event(
                    {
                        "event": "attempt_timeout",
                        "cache_key": cache_key,
                        "attempt": attempt + 1,
                        "status": "timeout",
                        "duration_s": duration_s,
                        "message": last_error[:400],
                    }
                )
                if attempt >= self.max_retries:
                    break
                time.sleep(1.5 * (attempt + 1))
                continue
            duration_s = round(time.time() - t0, 3)
            if payload:
                result = {
                    "structured_output": payload.get("structured_output"),
                    "raw_result": payload.get("result"),
                    "total_cost_usd": payload.get("total_cost_usd", 0.0),
                    "usage": payload.get("usage", {}),
                    "model_usage": payload.get("modelUsage", {}),
                    "duration_s": duration_s,
                    "cache_key": cache_key,
                    "cache_path": str(cache_path),
                }
                cache_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
                result["cache_hit"] = False
                self._log_event(
                    {
                        "event": "attempt_success",
                        "cache_key": cache_key,
                        "attempt": attempt + 1,
                        "status": "ok",
                        "duration_s": duration_s,
                        "message": f"wrote {cache_path.name}",
                    }
                )
                return result
            last_error = "backend returned empty payload"
            self._log_event(
                {
                    "event": "attempt_failure",
                    "cache_key": cache_key,
                    "attempt": attempt + 1,
                    "status": "empty_payload",
                    "duration_s": duration_s,
                    "message": last_error[:400],
                }
            )
            if attempt >= self.max_retries:
                break
            time.sleep(1.5 * (attempt + 1))

        self._log_event(
            {
                "event": "summarize_failed",
                "cache_key": cache_key,
                "status": "failed",
                "message": (last_error or "unknown error")[:400],
            }
        )
        raise RuntimeError(f"DeepSeek summarizer failed for {cache_key}: {last_error}")

    def _run_backend(
        self,
        *,
        prompt: str,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        if self.backend == "deepseek_cli":
            return self._run_deepseek_cli(prompt=prompt, schema=schema)
        if self.backend == "openai_compatible":
            return self._run_openai_compatible(prompt=prompt, schema=schema)
        raise RuntimeError(f"Unknown MEMORY_SUMMARIZER_BACKEND `{self.backend}`.")

    def _run_deepseek_cli(
        self,
        *,
        prompt: str,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        args = [
            "deepseek",
            "--bare",
            "--print",
            "--allowedTools",
            "",
            "--permission-mode",
            "dontAsk",
            "--output-format",
            "json",
            "--json-schema",
            json.dumps(schema, ensure_ascii=False),
            prompt,
        ]
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=self.timeout_s,
            check=False,
            cwd=str(self.run_cwd),
        )
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()
        if proc.returncode != 0 or not stdout:
            raise RuntimeError(stderr or stdout or f"deepseek returned code {proc.returncode}")
        try:
            return json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"invalid_json: {exc}: {stdout[:400]}") from exc

    def _run_openai_compatible(
        self,
        *,
        prompt: str,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        base_url = (os.environ.get("MEMORY_OPENAI_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or "").strip()
        api_key = (os.environ.get("MEMORY_OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY") or "").strip()
        model = (os.environ.get("MEMORY_OPENAI_MODEL") or os.environ.get("OPENAI_MODEL") or "").strip()
        if not base_url or not api_key or not model:
            raise RuntimeError("openai_compatible backend requires MEMORY_OPENAI_BASE_URL/API_KEY/MODEL (or OPENAI_* fallbacks).")
        payload: dict[str, Any] = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "memory_compaction",
                    "schema": schema,
                },
            },
        }
        if os.environ.get("MEMORY_OPENAI_MAX_TOKENS"):
            payload["max_tokens"] = int(os.environ["MEMORY_OPENAI_MAX_TOKENS"])
        elif os.environ.get("OPENAI_MAX_TOKENS"):
            payload["max_tokens"] = int(os.environ["OPENAI_MAX_TOKENS"])
        if os.environ.get("MEMORY_OPENAI_TEMPERATURE"):
            payload["temperature"] = float(os.environ["MEMORY_OPENAI_TEMPERATURE"])
        elif os.environ.get("OPENAI_TEMPERATURE"):
            payload["temperature"] = float(os.environ["OPENAI_TEMPERATURE"])
        request = urllib.request.Request(
            url=base_url.rstrip("/") + "/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"http_{exc.code}: {body[:400]}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"url_error: {exc.reason}") from exc
        message = (((response_payload.get("choices") or [{}])[0]).get("message") or {})
        content = message.get("content")
        if isinstance(content, list):
            content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError(f"empty_content: {json.dumps(response_payload)[:400]}")
        try:
            structured_output = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"invalid_json: {exc}: {content[:400]}") from exc
        return {
            "structured_output": structured_output,
            "result": content,
            "total_cost_usd": 0.0,
            "usage": response_payload.get("usage", {}),
            "modelUsage": response_payload.get("usage", {}),
        }
