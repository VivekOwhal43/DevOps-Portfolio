terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# 1. Create our own Custom Network (VPC)
resource "aws_vpc" "custom_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "DevOps-Portfolio-VPC"
  }
}

# 2. Create a Subnet (a smaller slice of the network)
resource "aws_subnet" "custom_subnet" {
  vpc_id                  = aws_vpc.custom_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true # Ensures our server gets a public IP address
  availability_zone       = "us-east-1a"
  tags = {
    Name = "DevOps-Portfolio-Subnet"
  }
}

# 3. Create the EC2 Instance and place it EXACTLY in our new Subnet
resource "aws_instance" "production_server" {
  ami           = "ami-0c7217cdde317cfec" 
  instance_type = "t2.micro"              
  subnet_id     = aws_subnet.custom_subnet.id # This line bypasses the error!

  tags = {
    Name = "DevOps-Portfolio-Server"
  }
}