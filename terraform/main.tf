# 1. Tell Terraform which cloud provider you are using
terraform {
    required_providers {
        aws = {
            source "hashicorp/aws"
            version: "~> 5.0"
        }
    }
}

# 2 configure the AWS provider (We will use the US East Region)

provider "aws" {
    region = "us-east-1"
}

# 3. Define the actual cloud resource (A free tier Liux server)
resource "aws_instance" "production_server" {
    ami           = "ami-0c7217cdde317cfec"  # This is the ID for a standard Ubuntu server on AWS
    instance_type = "t2.micro"               # This size is covered by aws FREE tier

    tags = {
        Name = "Devops-Portfolio-Server"
    }
}