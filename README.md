# ECS-Based Application Infrastructure

This project contains the infrastructure code for deploying a containerized application on AWS ECS using Terraform.

## Project Structure

The infrastructure is organized into modules:

- **Network Module**: VPC, subnets, internet gateway, NAT gateway, and route tables
- **Security Module**: Security groups and IAM roles
- **ECS Module**: ECS cluster, task definition, service, and ECR repository

## Deploying the Infrastructure

Follow these steps to deploy the infrastructure:

1. Initialize Terraform:
   ```bash
   terraform init
   ```

2. Review the execution plan:
   ```bash
   terraform plan
   ```

3. Apply the changes to create the infrastructure:
   ```bash
   terraform apply
   ```

4. When prompted, type `yes` to confirm the deployment.

5. After deployment, you can view the outputs:
   ```bash
   terraform output
   ```

6. To destroy the infrastructure when no longer needed:
   ```bash
   terraform destroy
   ```

## Remote State Management

This project separates remote state management from the main Terraform configuration. This allows you to:
1. Start with local state for development
2. Optionally use remote state for team collaboration

### Using Local State (Default)

By default, the project uses local state. To ensure you're using local state:

```bash
# Make the script executable
chmod +x use-local-state.sh

# Run the script
./use-local-state.sh
```

### How to Use Remote State

This project provides scripts to easily switch between local and remote state:

#### Using Local State (Default)
```bash
# Make the script executable
chmod +x use-local-state.sh

# Switch to local state
./use-local-state.sh
terraform init
terraform plan
```

#### Setting Up Remote State
```bash
# Make the scripts executable
chmod +x create-backend.sh
chmod +x use-remote-state.sh

# Create the required AWS resources
./create-backend.sh

# Configure Terraform to use remote state
./use-remote-state.sh
terraform plan
```

You can switch between local and remote state at any time using these scripts.

## Modules

### Network Module

Located in `modules/network`, this module creates:
- VPC with public and private subnets
- Internet Gateway for public internet access
- NAT Gateway for private subnet internet access
- Route tables for traffic routing

### Security Module

Located in `modules/security`, this module creates:
- Load balancer security group
- ECS tasks security group
- IAM roles for ECS task execution and task role

### ECS Module

Located in `modules/ecs`, this module creates:
- ECR repository for container images
- ECS cluster
- ECS task definition
- ECS service

## Application Description

This project deploys a Daily Task Manager application that helps users organize their daily activities. The application features:

- Task creation, retrieval, updating, and deletion
- Priority levels (1-5) for tasks
- Due dates and completion status tracking
- Web interface for viewing tasks
- RESTful API for backend functionality

The application is built with FastAPI and uses HTML templates for the frontend views.

## Running the Application Locally

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Setup and Run
1. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   uvicorn app:app --reload
   ```

5. Access the API:
   - Open your browser and navigate to http://localhost:8000
   - API documentation is available at http://localhost:8000/docs

### Using Docker
Alternatively, you can run the application using Docker:

```
docker build -t ecs-app .
docker run -p 8000:8000 ecs-app
```

## Infrastructure Usage

```hcl
module "network" {
  source = "./modules/network"
  
  project_name      = var.project_name
  vpc_cidr          = var.vpc_cidr
  availability_zones = var.availability_zones
}

module "security" {
  source = "./modules/security"
  
  project_name   = var.project_name
  vpc_id         = module.network.vpc_id
  container_port = var.container_port
}

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
```

## Future Improvements

- Create an ALB module to handle load balancer resources
- Add CloudWatch logging module
- Implement auto-scaling for ECS services

## Architecture Diagram

```
+-------------------+
|    Internet       |
+-------------------+
        |
        v
+-------------------+
| Application Load  |
|    Balancer (ALB) |
+-------------------+
        |
        v
+-------------------+
| ECS Cluster       |
| - ECS Service     |
| - ECS Task        |
+-------------------+
        |
        v
+-------------------+
| Private Subnets   |
+-------------------+
        |
        v
+-------------------+
| ECR Repository    |
+-------------------+
```