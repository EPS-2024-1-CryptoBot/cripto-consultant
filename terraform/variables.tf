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

variable "PG_USER" {
    type = string
    sensitive = true
}

variable "PG_PASS" {
    type = string
    sensitive = true
}

variable "PG_HOST" {
    type = string
    sensitive = true
}

variable "PG_DB" {
    type = string
    sensitive = true
}

variable "PG_SSL" {
    type = string
    sensitive = false
}

variable "DB_URL" {
    type = string
    sensitive = true
}