# Multi-Backbone Readiness

This artifact turns A2 into a concrete execution surface: which summarizer backbone profiles exist, and which ones are actually configured right now.

- multi-backbone ready: `False`
- ready profiles: `['deepseek_cli_default']`
- ready non-deepseek profiles: `[]`

| Profile | Backend | Ready | Missing env | DeepSeek CLI found |
|---|---|---|---|---|
| deepseek_cli_default | deepseek_cli | True | - | True |
| openai_default | openai_compatible | False | OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL | - |
| gpt_openai_profile | openai_compatible | False | GPT_OPENAI_API_KEY, GPT_OPENAI_BASE_URL, GPT_OPENAI_MODEL | - |
| qwen_openai_profile | openai_compatible | False | QWEN_OPENAI_API_KEY, QWEN_OPENAI_BASE_URL, QWEN_OPENAI_MODEL | - |
| llama_openai_profile | openai_compatible | False | LLAMA_OPENAI_API_KEY, LLAMA_OPENAI_BASE_URL, LLAMA_OPENAI_MODEL | - |

## Readout

- `deepseek_memory_summarizer.py` now supports both `deepseek_cli` and `openai_compatible` backends.
- This readiness table makes A2 falsifiable: we can now name exactly which additional backbone profiles are still missing.
- Once two non-DeepSeek profiles are configured, the next step is to launch the same staged benchmark under each profile and compare PSU retention / hallucination behavior across backbones.
