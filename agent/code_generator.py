import json
from agent.client import chat
from agent.context_builder import build_context

SYSTEM_PROMPT = open("prompts/code_generator.txt").read()

def generate_code(spec: dict) -> dict:
    context = build_context(spec)

    user_message = f"""
Infrastructure spec:
{json.dumps(spec, indent=2)}

Azure best practices and required resources for this spec:
{context}

Generate complete, production-grade Terraform code.
Return a JSON object with exactly these keys:
- main_tf      : complete main.tf content
- variables_tf : complete variables.tf content
- outputs_tf   : complete outputs.tf content
- tfvars       : complete terraform.tfvars content
"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_message}
    ]
    result = chat(messages, json_mode=True)
    return json.loads(result)