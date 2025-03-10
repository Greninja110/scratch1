import os
import django
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Users, Faculty, Student

class Command(BaseCommand):
    help = 'Initialize database with default users and data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database initialization...'))
        
        # Create default users
        self.create_default_users()
        
        self.stdout.write(self.style.SUCCESS('Database initialization completed successfully!'))
    
    def create_default_users(self):
        self.stdout.write('Creating default users...')
        
        # Define default users with different roles
        default_users = [
            {
                'username': 'admin@mbit.edu.in',
                'email': 'admin@mbit.edu.in',
                'password': '123',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'full_name': 'Admin User'
            },
            {
                'username': 'hod@mbit.edu.in',
                'email': 'hod@mbit.edu.in',
                'password': '123',
                'first_name': 'HOD',
                'last_name': 'User',
                'role': 'hod',
                'full_name': 'HOD User'
            },
            {
                'username': 'faculty@mbit.edu.in',
                'email': 'faculty@mbit.edu.in',
                'password': '123',
                'first_name': 'Faculty',
                'last_name': 'User',
                'role': 'faculty',
                'full_name': 'Faculty User'
            },
            {
                'username': 'labassistant@mbit.edu.in',
                'email': 'labassistant@mbit.edu.in',
                'password': '123',
                'first_name': 'Lab',
                'last_name': 'Assistant',
                'role': 'lab_assistant',
                'full_name': 'Lab Assistant'
            },
            {
                'username': 'student@mbit.edu.in',
                'email': 'student@mbit.edu.in',
                'password': '123',
                'first_name': 'Student',
                'last_name': 'User',
                'role': 'student',
                'full_name': 'Student User'
            }
        ]
        
        # Create user accounts
        for user_data in default_users:
            username = user_data['username']
            email = user_data['email']
            password = user_data['password']
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            role = user_data['role']
            full_name = user_data['full_name']
            
            # Check if user already exists
            if not User.objects.filter(username=username).exists():
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Create user profile
                user_profile = Users.objects.create(
                    user=user,
                    full_name=full_name,
                    role=role,
                    is_active=True
                )
                
                # Create additional profiles based on role
                if role == 'faculty':
                    Faculty.objects.create(
                        user=user,
                        employee_id='FAC001',
                        department='Computer Science',
                        designation='Assistant Professor',
                        joining_year=2022,
                        weekly_hours_limit=20,
                        current_weekly_hours=0
                    )
                elif role == 'student':
                    Student.objects.create(
                        user=user,
                        roll_number='CSE/2022/001',
                        batch_name='2022-2026',
                        admission_year=2022,
                        graduation_year=2026,
                        program='B.Tech',
                        department='Computer Science',
                        current_semester=4,
                        section='A'
                    )
                
                self.stdout.write(self.style.SUCCESS(f'Created {role} user: {username}'))
            else:
                self.stdout.write(f'User {username} already exists, skipping...')