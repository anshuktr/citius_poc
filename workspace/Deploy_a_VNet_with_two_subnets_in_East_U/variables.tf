variable "region" {
  description = "Azure region where resources will be created"
  type        = string
}

variable "environment" {
  description = "Environment tag for resources"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group to contain resources"
  type        = string
}

variable "owner" {
  description = "Owner tag for resources"
  type        = string
}

variable "naming_prefix" {
  description = "Prefix for resource naming"
  type        = string
}