variable "project_name" {
  description = "Project name to be used for resource naming"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "container_port" {
  description = "Port exposed by the container"
  type        = number
}

variable "alb_ingress_cidr_blocks" {
  description = "CIDR blocks to allow in ALB security group ingress rule"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "additional_task_role_policies" {
  description = "List of additional policy ARNs to attach to the ECS task role"
  type        = list(string)
  default     = []
}