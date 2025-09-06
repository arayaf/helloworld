#!/bin/bash

# STEM Learning Platform Startup Script

echo "🚀 Starting STEM Learning Platform..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your actual configuration values."
fi

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "📊 Running database migrations..."
docker-compose exec web python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
docker-compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin@stemlearning.com', 'admin123')
    print('Superuser created: admin@stemlearning.com / admin123')
else:
    print('Superuser already exists')
"

# Populate initial data
echo "📚 Populating initial STEM data..."
docker-compose exec web python manage.py populate_stem_data

# Collect static files
echo "📦 Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

echo "✅ STEM Learning Platform is ready!"
echo ""
echo "🌐 Web Application: http://localhost:8000"
echo "🔧 Admin Panel: http://localhost:8000/admin"
echo "📊 Database: localhost:5432"
echo ""
echo "👤 Admin Credentials:"
echo "   Email: admin@stemlearning.com"
echo "   Password: admin123"
echo ""
echo "📝 To stop the application, run: docker-compose down"
echo "📝 To view logs, run: docker-compose logs -f"