from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from typing import Any


class DeepSeekMemorySummarizer:
    def __init__(
        self,
        cache_dir: Path,
        timeout_s: int = 180,
        max_retries: int = 2,
        run_cwd: Path | None = None,
    ) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self.run_cwd = run_cwd or Path("/private/tmp")
        self.run_cwd.mkdir(parents=True, exist_ok=True)

    def summarize(
        self,
        *,
        cache_key: str,
        prompt: str,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        cache_path = self.cache_dir / f"{cache_key}.json"
        if cache_path.exists():
            return json.loads(cache_path.read_text(encoding="utf-8"))

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

        last_error: str | None = None
        for attempt in range(self.max_retries + 1):
            t0 = time.time()
            proc = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
                check=False,
                cwd=str(self.run_cwd),
            )
            duration_s = round(time.time() - t0, 3)
            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()
            if proc.returncode == 0 and stdout:
                payload = json.loads(stdout)
                result = {
                    "structured_output": payload.get("structured_output"),
                    "raw_result": payload.get("result"),
                    "total_cost_usd": payload.get("total_cost_usd", 0.0),
                    "usage": payload.get("usage", {}),
                    "model_usage": payload.get("modelUsage", {}),
                    "duration_s": duration_s,
                    "cache_key": cache_key,
                }
                cache_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
                return result
            last_error = stderr or stdout or f"deepseek returned code {proc.returncode}"
            if attempt >= self.max_retries:
                break
            time.sleep(1.5 * (attempt + 1))

        raise RuntimeError(f"DeepSeek summarizer failed for {cache_key}: {last_error}")
