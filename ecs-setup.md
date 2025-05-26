# ECS Setup Instructions

## 1. Create an ECR Repository
```bash
aws ecr create-repository \
    --repository-name ecs-app \
    --image-scanning-configuration scanOnPush=true
```

## 2. Configure GitHub Secrets
Add these secrets to your GitHub repository:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- ECR_REPOSITORY (ecs-app)
- ECR_REGISTRY (your-account-id.dkr.ecr.region.amazonaws.com)

## 3. Create an ECS Cluster
```bash
aws ecs create-cluster --cluster-name ecs-app-cluster
```

## 4. Create IAM Roles
```bash
# Task Execution Role
aws iam create-role \
    --role-name ecsTaskExecutionRole \
    --assume-role-policy-document file://trust-policy.json

aws iam attach-role-policy \
    --role-name ecsTaskExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

## 5. Create a Load Balancer
```bash
# Create a security group for the ALB
aws ec2 create-security-group \
    --group-name ecs-alb-sg \
    --description "Security group for ECS ALB" \
    --vpc-id vpc-xxxxxxxx

# Allow HTTP traffic
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxx \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

# Create the ALB
aws elbv2 create-load-balancer \
    --name ecs-app-alb \
    --subnets subnet-xxxxxxxx subnet-yyyyyyyy \
    --security-groups sg-xxxxxxxx
```

## 6. Create a Target Group
```bash
aws elbv2 create-target-group \
    --name ecs-app-tg \
    --protocol HTTP \
    --port 8000 \
    --vpc-id vpc-xxxxxxxx \
    --target-type ip \
    --health-check-path / \
    --health-check-interval-seconds 30
```

## 7. Create a Listener
```bash
aws elbv2 create-listener \
    --load-balancer-arn arn:aws:elasticloadbalancing:region:account-id:loadbalancer/app/ecs-app-alb/xxxxxxxx \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:region:account-id:targetgroup/ecs-app-tg/xxxxxxxx
```

## 8. Create an ECS Service
```bash
aws ecs create-service \
    --cluster ecs-app-cluster \
    --service-name ecs-app-service \
    --task-definition ecs-app-task \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxxxxx],securityGroups=[sg-xxxxxxxx],assignPublicIp=ENABLED}" \
    --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:region:account-id:targetgroup/ecs-app-tg/xxxxxxxx,containerName=ecs-app-container,containerPort=8000"
```

## 9. Access Your App
Once deployed, access your app via the ALB DNS name:
```bash
aws elbv2 describe-load-balancers \
    --names ecs-app-alb \
    --query 'LoadBalancers[0].DNSName' \
    --output text
```