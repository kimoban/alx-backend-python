#!/usr/bin/env python
"""
Setup script for Django Signals ORM Messaging App
This script helps set up the project with sample data
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and print its status."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    print("🚀 Setting up Django Signals ORM Messaging App")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)

    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("⚠️  Failed to install dependencies. Please install manually:")
        print("   pip install -r requirements.txt")

    # Create migrations
    run_command("python manage.py makemigrations", "Creating migrations")

    # Apply migrations
    run_command("python manage.py migrate", "Applying migrations")

    # Create superuser (optional)
    print("\n🔧 Creating superuser...")
    print("You can skip this step by pressing Ctrl+C")
    try:
        subprocess.run(["python", "manage.py", "createsuperuser"], check=True)
        print("✅ Superuser created successfully")
    except KeyboardInterrupt:
        print("\n⏭️  Skipping superuser creation")
    except subprocess.CalledProcessError:
        print("⚠️  Superuser creation failed or was skipped")

    # Create sample data
    if run_command("python manage.py create_sample_data --users=5 --messages=20", "Creating sample data"):
        print("✅ Sample data created successfully")

    # Final instructions
    print("\n🎉 Setup completed!")
    print("=" * 50)
    print("📋 Next steps:")
    print("1. Start the development server:")
    print("   python manage.py runserver")
    print("\n2. Open your browser and visit:")
    print("   • Admin interface: http://127.0.0.1:8000/admin/")
    print("   • Messaging app: http://127.0.0.1:8000/messaging/")
    print("   • Chat conversations: http://127.0.0.1:8000/chats/")
    print("\n3. Login with sample users:")
    print("   • Username: user1, user2, user3, user4, user5")
    print("   • Password: password123")
    print("\n4. Test the features:")
    print("   • Send messages and see notifications (Task 0)")
    print("   • Edit messages and view history (Task 1)")
    print("   • Test threaded conversations (Task 3)")
    print("   • Check unread message filters (Task 4)")
    print("   • Observe view caching (Task 5)")
    print("\n5. Run tests:")
    print("   python manage.py test messaging")

if __name__ == "__main__":
    main()
