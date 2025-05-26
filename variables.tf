variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name to be used for resource naming"
  type        = string
  default     = "ecs-app"
}

variable "ecr_repository_name" {
  description = "Name of ECR repository"
  type        = string
  default     = "ecs-app"
}

variable "container_port" {
  description = "Port exposed by the container"
  type        = number
  default     = 8000
}

variable "container_cpu" {
  description = "The number of cpu units to reserve for the container"
  type        = number
  default     = 256
}

variable "container_memory" {
  description = "The amount of memory to reserve for the container"
  type        = number
  default     = 512
}

variable "app_count" {
  description = "Number of containers to run"
  type        = number
  default     = 1
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "alb_ingress_cidr_blocks" {
  description = "CIDR blocks to allow in ALB security group ingress rule"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}