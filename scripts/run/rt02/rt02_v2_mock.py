#!/usr/bin/env python3
"""RT-02 v2 mock OpenAI chat client — offline end-to-end pipeline validation ONLY.

Lets the v2 runners exercise the full control flow (retrieval -> genuine operator ->
official generate_response -> official judge -> snapshot/records/fail-fast) with ZERO
API cost and deterministic output. Mock endpoints are semantically MEANINGLESS: the
mock judge returns a hash-derived SAFE/MISLED so endpoints show variance for the
"endpoint has variance" smoke check. Never use mock output for any research verdict.
"""
import hashlib
import json


class _Msg:
    def __init__(self, content):
        self.content = content


class _Choice:
    def __init__(self, content):
        self.message = _Msg(content)


class _Resp:
    def __init__(self, content):
        self.choices = [_Choice(content)]


class _Completions:
    def __init__(self, parent):
        self.parent = parent

    def create(self, model=None, messages=None, temperature=0, **kw):
        prompt = (messages or [{}])[-1].get("content", "")
        return _Resp(self.parent._respond(prompt))


class _Chat:
    def __init__(self, parent):
        self.completions = _Completions(parent)


class MockChatClient:
    def __init__(self, seed=20260719):
        self.chat = _Chat(self)
        self.calls = {"judge": 0, "trustmem": 0, "gen": 0}
        self.seed = seed

    def _h(self, s):
        return int(hashlib.sha256(f"{self.seed}|{s}".encode("utf-8")).hexdigest(), 16)

    def _respond(self, prompt):
        # official QA judge prompt carries the literal JSON key instruction
        if '"verdict"' in prompt and '"risk_exhibited"' in prompt:
            self.calls["judge"] += 1
            verdict = "MISLED" if self._h(prompt) % 2 == 0 else "SAFE"
            return json.dumps({"risk_exhibited": verdict == "MISLED",
                               "verdict": verdict, "reason": "mock judge (offline validation only)"})
        if '"coverage"' in prompt and '"faithfulness"' in prompt:
            self.calls["trustmem"] += 1
            h = self._h(prompt)
            return json.dumps({"coverage": 5 + h % 6, "preservation": 5 + (h // 7) % 6,
                               "faithfulness": 5 + (h // 13) % 6})
        self.calls["gen"] += 1
        return f"MOCK_ANSWER[{self._h(prompt) % 100000}] (offline pipeline validation, not a real response)"
