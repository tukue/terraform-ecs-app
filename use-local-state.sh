#!/bin/bash

# Script to configure Terraform to use local state

echo "Configuring Terraform to use local state..."

# Remove backend.tf if it exists
if [ -f backend.tf ]; then
  rm backend.tf
  echo "Removed backend.tf"
fi

# Initialize Terraform with local backend
echo "Initializing Terraform with local backend..."
terraform init -reconfigure

echo "Terraform is now configured to use local state"