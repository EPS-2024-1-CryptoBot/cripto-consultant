resource "aws_iam_role" "consultant_api_role" {
    name   = "consultant_API_Role"
    assume_role_policy = jsonencode(
            {
                "Version": "2012-10-17",
                "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Principal": {
                    "Service": "lambda.amazonaws.com"
                    },
                    "Effect": "Allow",
                    "Sid": ""
                }
                ]
            }
        )
}