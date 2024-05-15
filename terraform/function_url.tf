resource "aws_lambda_function_url" "consultant_api_url" {
  function_name      = aws_lambda_function.terraform_lambda_func.function_name
  authorization_type = "NONE"
}