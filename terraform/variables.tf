data "aws_caller_identity" "current" {}

variable "environment" {
    type = string
    sensitive = false
}