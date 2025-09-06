# STEM Learning Platform

A comprehensive web application designed specifically for first-year engineering students to master STEM fundamentals.

## Features

- **Comprehensive STEM Curriculum**: Mathematics, Physics, Chemistry, and Computer Science
- **Interactive Learning**: Lessons, quizzes, and progress tracking
- **Google OAuth Authentication**: Secure login with Google accounts
- **Separate Database Server**: PostgreSQL database running on a separate server
- **Crimson Theme**: Beautiful, modern UI with crimson color scheme
- **Study Groups**: Collaborative learning features
- **Formula Reference**: Quick access to essential formulas and equations
- **Progress Tracking**: Detailed analytics of learning progress

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL 15
- **Authentication**: Django Allauth with Google OAuth
- **Frontend**: Bootstrap 5, Font Awesome
- **Deployment**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Google OAuth credentials (for authentication)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stem-learning-platform
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. **Configure Google OAuth**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Add your domain to authorized origins
   - Update `GOOGLE_OAUTH2_CLIENT_ID` and `GOOGLE_OAUTH2_CLIENT_SECRET` in `.env`

4. **Start the application**
   ```bash
   docker-compose up --build
   ```

5. **Run database migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

7. **Populate initial data**
   ```bash
   docker-compose exec web python manage.py populate_stem_data
   ```

8. **Access the application**
   - Web app: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Project Structure

```
stem-learning-platform/
├── core/                    # Core app (home, about, contact)
├── users/                   # User management and profiles
├── stem/                    # STEM content and learning features
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── stem_learning/          # Django project settings
├── requirements.txt         # Python dependencies
├── docker-compose.yml      # Docker services configuration
├── Dockerfile              # Docker image configuration
└── README.md               # This file
```

## Database Configuration

The application uses PostgreSQL running on a separate server:

- **Host**: `db` (Docker service name)
- **Port**: `5432`
- **Database**: `stem_learning_db`
- **User**: `stem_user`
- **Password**: `stem_password`

## Features Overview

### Subjects
- Mathematics (Calculus, Linear Algebra)
- Physics (Classical Mechanics, Thermodynamics)
- Chemistry (General Chemistry, Organic Chemistry)
- Computer Science (Programming, Data Structures)

### Learning Features
- **Lessons**: Structured content with theory, examples, and exercises
- **Quizzes**: Interactive questions to test understanding
- **Progress Tracking**: Monitor completion and scores
- **Formulas**: Quick reference for essential equations
- **Study Groups**: Collaborative learning environment

### User Management
- Google OAuth authentication
- User profiles with academic information
- Progress tracking and analytics
- Achievement system

## Development

### Running in Development Mode

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database**
   ```bash
   # Install PostgreSQL locally or use Docker
   docker run --name postgres-db -e POSTGRES_DB=stem_learning_db -e POSTGRES_USER=stem_user -e POSTGRES_PASSWORD=stem_password -p 5432:5432 -d postgres:15
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Adding New Content

1. **Create new subjects/topics/lessons** through the admin panel
2. **Use management commands** to populate bulk data
3. **Add formulas** through the Formula model

## Deployment

### Production Deployment

1. **Update environment variables**
   - Set `DEBUG=False`
   - Configure production database URL
   - Set up proper Google OAuth credentials
   - Configure email settings

2. **Use production WSGI server**
   ```bash
   gunicorn stem_learning.wsgi:application
   ```

3. **Set up reverse proxy** (nginx recommended)

4. **Configure SSL certificates**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact us at support@stemlearning.com