provider "aws" {
  region = var.aws_region
}

# Network Module
module "network" {
  source = "./modules/network"
  
  project_name      = var.project_name
  vpc_cidr          = var.vpc_cidr
  availability_zones = var.availability_zones
}

# Security Module
module "security" {
  source = "./modules/security"
  
  project_name   = var.project_name
  vpc_id         = module.network.vpc_id
  container_port = var.container_port
  alb_ingress_cidr_blocks = var.alb_ingress_cidr_blocks
}

# ALB Module
module "alb" {
  source = "./modules/alb"
  
  project_name        = var.project_name
  vpc_id              = module.network.vpc_id
  public_subnet_ids   = module.network.public_subnet_ids
  lb_security_group_id = module.security.lb_security_group_id
  container_port      = var.container_port
}

# ECS Module
module "ecs" {
  source = "./modules/ecs"
  
  aws_region        = var.aws_region
  project_name      = var.project_name
  ecr_repository_name = var.ecr_repository_name
  container_port    = var.container_port
  container_cpu     = var.container_cpu
  container_memory  = var.container_memory
  app_count         = var.app_count
  
  ecs_task_execution_role_arn = module.security.ecs_task_execution_role_arn
  ecs_task_role_arn           = module.security.ecs_task_role_arn
  ecs_tasks_security_group_id = module.security.ecs_tasks_security_group_id
  private_subnet_ids          = module.network.private_subnet_ids
  
  target_group_arn = module.alb.target_group_arn
  lb_listener_arn  = module.alb.lb_listener_arn
}