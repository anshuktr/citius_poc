import json
from agent.client import chat

SYSTEM_PROMPT = """
You are an Azure infrastructure expert. Extract a structured specification
from the user's natural language infrastructure request.

Return ONLY valid JSON with this exact schema:
{
  "resources": ["list of azure resource types needed"],
  "region": "azure region slug e.g. eastus",
  "environment": "dev | staging | production",
  "constraints": { "key": "value pairs for special requirements" },
  "naming_prefix": "short lowercase prefix for resource names"
}

Rules:
- resources must be from: aks, vnet, acr, keyvault
- Never add explanation or markdown — raw JSON only
"""

def parse_intent(user_request: str) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_request}
    ]
    raw = chat(messages, json_mode=True)
    return json.loads(raw)