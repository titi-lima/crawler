terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = "sa-east-1"
  access_key = var.access_key
  secret_key = var.secret_key
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"
    
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "titi-lima-my-lambda-deployment-bucket"
}

resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.lambda_bucket.id
  key    = "lambda_function_payload.zip"
  source = "${path.module}/lambda_function_payload.zip"
  etag   = filemd5("${path.module}/lambda_function_payload.zip")
}

resource "aws_lambda_function" "test_lambda" {
  s3_bucket        = aws_s3_bucket.lambda_bucket.id
  s3_key           = aws_s3_object.lambda_zip.key
  function_name    = "lambda_function_name"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "main.handler"
  
  source_code_hash = filebase64sha256("${path.module}/lambda_function_payload.zip")

  runtime = "python3.10"

  environment {
    variables = {
      "API_KEY" = "${var.api_key}"
    }
  }
}

resource "aws_apigatewayv2_api" "api" {
  name          = "example-api"
  protocol_type = "HTTP"
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.test_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*"
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id             = aws_apigatewayv2_api.api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.test_lambda.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "lambda" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.api.api_endpoint
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.test_lambda.function_name}"
  retention_in_days = 7
}

resource "aws_iam_role_policy" "lambda_logging" {
  name   = "lambda_logging_policy"
  role   = aws_iam_role.iam_for_lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_dynamodb_table" "receipts" {
  name           = "receipts"
  billing_mode   = "PAY_PER_REQUEST"

  hash_key       = "id"        # Partition key
  range_key      = "date"      # Sort key

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }

  tags = {
    Environment = "production"
    Name        = "ReceiptsTable"
  }
}