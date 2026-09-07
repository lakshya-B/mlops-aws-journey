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