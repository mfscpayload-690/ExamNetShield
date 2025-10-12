#!/usr/bin/env python3
"""
Create admin user for ExamNetShield.

This script creates the initial admin user for the application.
Run this once during initial setup.
"""
from app import app, db
from models import User
import getpass
import sys


def create_admin_user():
    """Create an admin user with interactive password input."""
    print("=== ExamNetShield Admin User Creation ===\n")
    
    # Get username
    while True:
        username = input("Enter admin username (default: admin): ").strip()
        if not username:
            username = "admin"
        
        if len(username) < 3:
            print("Error: Username must be at least 3 characters long.\n")
            continue
            
        break
    
    # Get password
    while True:
        password = getpass.getpass("Enter admin password: ")
        
        if len(password) < 6:
            print("Error: Password must be at least 6 characters long.\n")
            continue
        
        password_confirm = getpass.getpass("Confirm admin password: ")
        
        if password != password_confirm:
            print("Error: Passwords do not match.\n")
            continue
            
        break
    
    # Initialize the database and create the admin user
    with app.app_context():
        try:
            db.create_all()
            
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print(f"\nError: User '{username}' already exists!")
                overwrite = input("Do you want to update the password? (yes/no): ").lower()
                if overwrite != 'yes':
                    print("User creation cancelled.")
                    return
                
                existing_user.password = User(username, password).password
                db.session.commit()
                print(f"\nPassword updated for user '{username}'!")
            else:
                admin_user = User(username=username, password=password)
                db.session.add(admin_user)
                db.session.commit()
                print(f"\nAdmin user '{username}' created successfully!")
            
            print("\nYou can now login to the application with these credentials.")
            print("Please keep your credentials secure!")
            
        except Exception as e:
            print(f"\nError creating user: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    create_admin_user()