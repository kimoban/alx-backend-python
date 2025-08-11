from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from messaging.models import Message, Notification


class Command(BaseCommand):
    help = 'Create sample data for testing the messaging app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=3,
            help='Number of users to create',
        )
        parser.add_argument(
            '--messages',
            type=int,
            default=10,
            help='Number of messages to create',
        )

    def handle(self, *args, **options):
        users_count = options['users']
        messages_count = options['messages']

        self.stdout.write('Creating sample data...')

        # Create users if they don't exist
        users = []
        for i in range(1, users_count + 1):
            username = f'user{i}'
            email = f'user{i}@example.com'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'User',
                    'last_name': f'{i}',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {username}')
            users.append(user)

        # Create messages
        import random
        from django.utils import timezone
        from datetime import timedelta

        for i in range(messages_count):
            sender = random.choice(users)
            receiver = random.choice([u for u in users if u != sender])
            
            # Create some threaded conversations
            parent_message = None
            if i > 5 and random.choice([True, False]):
                # 50% chance to create a reply for later messages
                existing_messages = Message.objects.filter(
                    sender=receiver, receiver=sender
                ).exclude(parent_message__isnull=False)
                if existing_messages.exists():
                    parent_message = random.choice(existing_messages)

            message_content = [
                "Hello! How are you doing today?",
                "Thanks for your message yesterday.",
                "Can we schedule a meeting this week?",
                "I hope you're having a great day!",
                "Let me know when you're available.",
                "This is an important update.",
                "Just wanted to check in with you.",
                "Hope everything is going well.",
                "Looking forward to hearing from you.",
                "Have a wonderful weekend!",
            ]

            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=random.choice(message_content) + f" (Message {i+1})",
                parent_message=parent_message,
                timestamp=timezone.now() - timedelta(hours=random.randint(0, 72))
            )

            # Randomly mark some messages as read
            if random.choice([True, False, False]):  # 33% chance to be read
                message.read = True
                message.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {users_count} users and {messages_count} messages'
            )
        )

        # Display statistics
        total_users = User.objects.count()
        total_messages = Message.objects.count()
        total_notifications = Notification.objects.count()
        unread_messages = Message.objects.filter(read=False).count()

        self.stdout.write(f'Statistics:')
        self.stdout.write(f'  Total Users: {total_users}')
        self.stdout.write(f'  Total Messages: {total_messages}')
        self.stdout.write(f'  Total Notifications: {total_notifications}')
        self.stdout.write(f'  Unread Messages: {unread_messages}')

        self.stdout.write('\nYou can now:')
        self.stdout.write('1. Run the server: python manage.py runserver')
        self.stdout.write('2. Visit /admin/ to see the data')
        self.stdout.write('3. Visit /messaging/ to use the messaging interface')
        self.stdout.write('4. Login with any user (password: password123)')
