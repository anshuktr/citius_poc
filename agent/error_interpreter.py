import json
from agent.client import chat

SYSTEM_PROMPT = open("prompts/error_interpreter.txt").read()

def interpret_errors(errors: list, current_code: dict) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Validation errors:
{json.dumps(errors, indent=2)}

Current generated code:
{json.dumps(current_code, indent=2)}
"""}
    ]
    raw = chat(messages, json_mode=True)
    return json.loads(raw)