provider "aws" {
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  access_key                  = "mock"
  secret_key                  = "mock"
  region                      = "ap-southeast-1"
  s3_use_path_style           = true

  endpoints {
    s3 = "http://localhost:4566"
  }
}

resource "aws_s3_bucket" "poc_s3_bucket" {
  bucket = "poc-s3-bucket"
}