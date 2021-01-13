data "archive_file" "send-email" {
  type        = "zip"
  output_path = "./send-email.zip"
  source_dir  = "./code/send_email"
}

resource "aws_iam_role" "iam_role_for_lambda" {
  name               = "${var.workspace_name}_iam_role_for_lambda"
  assume_role_policy = <<EOF
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
EOF
}

resource "aws_lambda_function" "sample_lambda" {
  filename         = "send-email.zip"
  function_name    = "${var.workspace_name}_send-email-demo"
  role             = aws_iam_role.iam_role_for_lambda.arn
  handler          = "dns_email.lambda_handler"
  source_code_hash = data.archive_file.send-email.output_base64sha256
  runtime          = "python3.7"
  depends_on       = [data.archive_file.send-email]
  timeout          = 900
}
