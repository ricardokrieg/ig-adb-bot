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
  count                  = 1
  ami                    = "ami-0ccf2d40012a1d067"
  instance_type          = "t3.small"
  key_name               = "ricardo_aws"
  vpc_security_group_ids = ["sg-06c24e62aa6a8e8b2"]

  tags = {
    Terraform = "true"
    Instagram = "true"
  }

  provisioner "local-exec" {
    command = "sleep 120; echo Installing on ${self.id}...; sh install.sh ${self.id} ${self.private_ip}; echo Done!"
  }

  provisioner "local-exec" {
    command = "echo Sign up on ${self.id}; python3 ../signup.py ${self.private_ip}:5555 'Casas Bahia' casasbahia.jpeg; echo Done!"
  }
}
