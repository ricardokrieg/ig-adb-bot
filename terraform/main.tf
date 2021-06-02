terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_instance" "genymotion" {
  count                  = 2
  ami                    = "ami-0ccf2d40012a1d067"
  instance_type          = "t3.small"
  key_name               = "ricardo_aws"
  vpc_security_group_ids = ["sg-0c51c3a1bdfb35688"]

  tags = {
    Instagram = "true"
  }
}
