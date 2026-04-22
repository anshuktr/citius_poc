AZURE_CONTEXT = {
    "aks": {
        "description": "Azure Kubernetes Service cluster",
        "best_practices": [
            "Use SystemAssigned managed identity",
            "Enable private cluster for production",
            "Set network_plugin to azure",
            "Always specify kubernetes_version",
            "Use Standard_D2s_v3 or larger for node VMs"
        ],
        "required_resources": [
            "azurerm_kubernetes_cluster"
        ],
        "depends_on": ["vnet"]
    },
    "vnet": {
        "description": "Azure Virtual Network with subnets",
        "best_practices": [
            "Use /16 address space for the VNet",
            "Create separate subnets for AKS, App Gateway, private endpoints",
            "Never use the default subnet"
        ],
        "required_resources": [
            "azurerm_virtual_network",
            "azurerm_subnet"
        ],
        "depends_on": []
    },
    "acr": {
        "description": "Azure Container Registry",
        "best_practices": [
            "Use Premium SKU for production with geo-replication",
            "Disable admin_enabled, use managed identity instead",
            "Attach ACR to AKS using role assignment"
        ],
        "required_resources": [
            "azurerm_container_registry",
            "azurerm_role_assignment"
        ],
        "depends_on": []
    },
    "keyvault": {
        "description": "Azure Key Vault for secrets management",
        "best_practices": [
            "Enable soft_delete_retention_days >= 7",
            "Enable purge_protection_enabled in production",
            "Use RBAC authorization instead of access policies",
            "Enable private endpoint in production"
        ],
        "required_resources": [
            "azurerm_key_vault"
        ],
        "depends_on": []
    }
}

def build_context(spec: dict) -> str:
    resources = spec.get("resources", [])
    context_parts = []

    for resource in resources:
        key = resource.lower().strip()
        if key in AZURE_CONTEXT:
            info = AZURE_CONTEXT[key]
            practices = "\n".join(f"  - {p}" for p in info["best_practices"])
            required   = ", ".join(info["required_resources"])
            context_parts.append(f"""
### {key.upper()} — {info['description']}
Required azurerm resources: {required}
Best practices:
{practices}
""")

    return "\n".join(context_parts)