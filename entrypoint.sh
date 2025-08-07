#!/bin/bash

# Wait for MySQL database to be ready
echo "Waiting for MySQL database..."
while ! mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" &> /dev/null; do
  echo "MySQL is unavailable - sleeping"
  sleep 2
done
echo "MySQL is up and running!"

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Start the Django development server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
