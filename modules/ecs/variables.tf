variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "project_name" {
  description = "Project name to be used for resource naming"
  type        = string
}

variable "ecr_repository_name" {
  description = "Name of ECR repository"
  type        = string
}

variable "container_port" {
  description = "Port exposed by the container"
  type        = number
}

variable "container_cpu" {
  description = "The number of cpu units to reserve for the container"
  type        = number
}

variable "container_memory" {
  description = "The amount of memory to reserve for the container"
  type        = number
}

variable "app_count" {
  description = "Number of containers to run"
  type        = number
}

variable "ecs_task_execution_role_arn" {
  description = "ARN of the ECS task execution role"
  type        = string
}

variable "ecs_task_role_arn" {
  description = "ARN of the ECS task role"
  type        = string
}

variable "ecs_tasks_security_group_id" {
  description = "ID of the ECS tasks security group"
  type        = string
}

variable "private_subnet_ids" {
  description = "IDs of the private subnets"
  type        = list(string)
}

variable "target_group_arn" {
  description = "ARN of the target group"
  type        = string
}

variable "lb_listener_arn" {
  description = "ARN of the load balancer listener"
  type        = string
}