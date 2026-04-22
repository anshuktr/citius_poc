output "vnet_id" {
  description = "ID of the created Virtual Network"
  value       = azurerm_virtual_network.vnet.id
}

output "aks_subnet_id" {
  description = "ID of the AKS subnet"
  value       = azurerm_subnet.aks_subnet.id
}

output "app_gateway_subnet_id" {
  description = "ID of the App Gateway subnet"
  value       = azurerm_subnet.app_gateway_subnet.id
}

output "private_endpoint_subnet_id" {
  description = "ID of the Private Endpoint subnet"
  value       = azurerm_subnet.private_endpoint_subnet.id
}