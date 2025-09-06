#!/usr/bin/env python
"""
Development server runner for STEM Learning Platform
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stem_learning.settings')
    django.setup()
    
    # Run migrations
    print("Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser if it doesn't exist
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        print("Creating superuser...")
        execute_from_command_line(['manage.py', 'createsuperuser', '--noinput', '--email', 'admin@stemlearning.com'])
        # Set password for the superuser
        admin_user = User.objects.get(email='admin@stemlearning.com')
        admin_user.set_password('admin123')
        admin_user.save()
        print("Superuser created: admin@stemlearning.com / admin123")
    
    # Populate initial data
    print("Populating initial STEM data...")
    execute_from_command_line(['manage.py', 'populate_stem_data'])
    
    # Start development server
    print("Starting development server...")
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])