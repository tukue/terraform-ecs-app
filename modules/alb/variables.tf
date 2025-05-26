variable "project_name" {
  description = "Project name to be used for resource naming"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "public_subnet_ids" {
  description = "IDs of the public subnets"
  type        = list(string)
}

variable "lb_security_group_id" {
  description = "ID of the load balancer security group"
  type        = string
}

variable "container_port" {
  description = "Port exposed by the container"
  type        = number
}