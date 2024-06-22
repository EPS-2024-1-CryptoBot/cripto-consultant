data "aws_caller_identity" "current" {}

variable "environment" {
    type = string
    sensitive = false
}

variable "COIN_GECKO_API_KEY" {
    type = string
    sensitive = true
}

variable "COIN_GECKO_API_URL" {
    type = string
    sensitive = false
}

variable "DB_URL" {
    type = string
    sensitive = true
}

variable "DB_SCHEMA" {
    type = string
    sensitive = true
}