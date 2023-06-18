provider "aws" {
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  access_key                  = "mock"
  secret_key                  = "mock"
  region                      = "us-east-1"
  s3_use_path_style           = true

  endpoints {
    s3  = "http://localhost:4566"
    sqs = "http://localhost:4566"
    sns = "http://localhost:4566"
  }
}

resource "aws_s3_bucket" "poc_s3_bucket" {
  bucket = "poc-s3-bucket"
}

resource "aws_sqs_queue" "poc_queue" {
  name = "poc-queue"
}

resource "aws_sns_topic" "poc_topic" {
  name = "poc-topic"
}

resource "aws_sns_topic_subscription" "example_subscription" {
  topic_arn = aws_sns_topic.poc_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.poc_queue.arn
}