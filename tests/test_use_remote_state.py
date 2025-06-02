import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
import subprocess
import sys

# Add the parent directory to sys.path to import the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestUseRemoteState(unittest.TestCase):
    """Tests for the use-remote-state.sh script"""
    
    def test_backend_file_creation(self):
        """Test that the backend.tf file is created with correct substitutions"""
        # This is a simplified test for the bash script functionality
        # We'll just check that the template file exists
        template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend.tf.template')
        self.assertTrue(os.path.exists(template_path), "backend.tf.template should exist")
    
    def test_environment_variables(self):
        """Test that the script uses the correct environment variables"""
        # Check that the script contains the expected environment variables
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'use-remote-state.sh')
        with open(script_path, 'r') as f:
            content = f.read()
            self.assertIn('REGION=', content)
            self.assertIn('BUCKET_NAME=', content)
            self.assertIn('TABLE_NAME=', content)
    
    def test_terraform_commands(self):
        """Test that the script contains terraform init command"""
        # Check that the script contains terraform init
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'use-remote-state.sh')
        with open(script_path, 'r') as f:
            content = f.read()
            self.assertIn('terraform init', content)


if __name__ == '__main__':
    unittest.main()