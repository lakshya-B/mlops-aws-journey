# 1. Tell terraform to use the AWS provider
terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~>5.0"
        }
    }
}

# 2. Configure the AWS provider region (automatically pulls keys from our 'aws configure')
provider "aws" {
    region = "us-east-1"
}

# 3. Declare a brand new s3 bucket for the production registry
resource "aws_s3_bucket" "ml_registry" {
    bucket = "aku-terraform-registry-2026"

    tags = {
        Environment = "Dev"
        ManagedBy = "terraform"
    }
}

# 1. Enable object versioning on our terraform-mamnged bucket
resource "aws_s3_bucket_versioning" "ml_registry_versioning" {
    bucket = aws_s3_bucket.ml_registry.id
    versioning_configuration {
        status = "Enabled"
    }
}

# 2. configure the lifecycle policy to move old models to glacier archiving after 30 days
resource "aws_s3_bucket_lifecycle_configuration" "ml_registry_lifecycle" {
    bucket = aws_s3_bucket.ml_registry.id
    rule {
        id = "archive-old-model-versions"
        status = "Enabled"

        filter {
            prefix = "models/"
        }
        # transition historical (non-current) versions to glacier
        noncurrent_version_transition {
            noncurrent_days = 30
            storage_class = "GLACIER"
        }
    }
}