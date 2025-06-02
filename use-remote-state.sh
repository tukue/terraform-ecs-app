#!/bin/bash

# Script to configure Terraform to use remote state

# Configuration
REGION="eu-north-1"
BUCKET_NAME="jenkins-tfstate-dev-2025"
TABLE_NAME="terraform-lock"

echo "Configuring Terraform to use remote state..."

# Create backend.tf from template
cat backend.tf.template | \
  sed "s/BUCKET_NAME/$BUCKET_NAME/g" | \
  sed "s/REGION/$REGION/g" | \
  sed "s/TABLE_NAME/$TABLE_NAME/g" > backend.tf

echo "Created backend.tf with S3 configuration"

# Initialize Terraform with the new backend
echo "Initializing Terraform with remote backend..."
terraform init -reconfigure

echo "Terraform is now configured to use remote state in S3"