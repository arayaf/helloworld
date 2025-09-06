# STEM Learning Platform - Setup Guide

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

1. **Start the application**
   ```bash
   ./start.sh
   ```

2. **Access the application**
   - Web app: http://localhost:8000
   - Admin panel: http://localhost:8000/admin
   - Database: localhost:5432

3. **Default admin credentials**
   - Email: admin@stemlearning.com
   - Password: admin123

### Option 2: Manual Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database**
   ```bash
   # Using Docker
   docker run --name postgres-db -e POSTGRES_DB=stem_learning_db -e POSTGRES_USER=stem_user -e POSTGRES_PASSWORD=stem_password -p 5432:5432 -d postgres:15
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate initial data**
   ```bash
   python manage.py populate_stem_data
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add your domain to authorized origins
6. Update `.env` file:
   ```
   GOOGLE_OAUTH2_CLIENT_ID=your-client-id
   GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret
   ```

### Database Configuration

The application uses PostgreSQL on a separate server:

- **Development**: `postgresql://stem_user:stem_password@localhost:5432/stem_learning_db`
- **Production**: Update `DATABASE_URL` in `.env`

### Email Configuration

For production, configure SMTP settings in `.env`:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📚 Features Overview

### Subjects Available
- **Mathematics**: Calculus, Linear Algebra, Statistics
- **Physics**: Classical Mechanics, Thermodynamics, Electromagnetism
- **Chemistry**: General Chemistry, Organic Chemistry
- **Computer Science**: Programming, Data Structures, Algorithms

### Learning Features
- **Interactive Lessons**: Theory, examples, and exercises
- **Quizzes**: Multiple choice, true/false, fill-in-the-blank
- **Progress Tracking**: Monitor completion and scores
- **Formula Reference**: Quick access to essential equations
- **Study Groups**: Collaborative learning environment

### User Management
- **Google OAuth**: Secure authentication
- **User Profiles**: Academic information and progress
- **Achievement System**: Badges and certificates
- **Progress Analytics**: Detailed learning statistics

## 🎨 Crimson Theme

The application features a beautiful crimson theme with:
- Primary color: #DC143C (Crimson)
- Dark variant: #B22222
- Light variant: #FF6B6B
- Responsive design with Bootstrap 5
- Modern UI components with smooth animations

## 🗄️ Database Schema

### Core Models
- **User**: Custom user model with academic information
- **Subject**: STEM subjects (Math, Physics, Chemistry, CS)
- **Topic**: Topics within each subject
- **Lesson**: Individual lessons with content
- **Quiz**: Interactive questions and answers
- **Formula**: Mathematical and scientific formulas
- **StudyGroup**: Collaborative learning groups

### Progress Tracking
- **UserProgress**: Overall learning progress
- **UserLessonProgress**: Individual lesson completion
- **UserQuizAttempt**: Quiz attempt history

## 🚀 Deployment

### Production Deployment

1. **Update settings**
   ```bash
   # Use production settings
   export DJANGO_SETTINGS_MODULE=stem_learning.settings_production
   ```

2. **Configure environment**
   - Set `DEBUG=False`
   - Configure production database
   - Set up proper Google OAuth credentials
   - Configure email settings

3. **Deploy with Gunicorn**
   ```bash
   gunicorn stem_learning.wsgi:application
   ```

4. **Set up reverse proxy** (nginx recommended)

5. **Configure SSL certificates**

### Docker Production

1. **Build production image**
   ```bash
   docker build -t stem-learning-prod .
   ```

2. **Run with production settings**
   ```bash
   docker run -e DJANGO_SETTINGS_MODULE=stem_learning.settings_production stem-learning-prod
   ```

## 🔍 Troubleshooting

### Common Issues

1. **Database connection error**
   - Check PostgreSQL is running
   - Verify database credentials in `.env`
   - Ensure database exists

2. **Google OAuth not working**
   - Check client ID and secret in `.env`
   - Verify authorized origins in Google Console
   - Ensure Google+ API is enabled

3. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` and `STATIC_URL` settings

4. **Migration errors**
   - Check database permissions
   - Verify model changes
   - Run `python manage.py makemigrations` if needed

### Logs

- **Docker logs**: `docker-compose logs -f`
- **Django logs**: Check `logs/django.log`
- **Database logs**: Check PostgreSQL logs

## 📞 Support

For support and questions:
- Email: support@stemlearning.com
- Documentation: Check README.md
- Issues: Create GitHub issue

## 🎯 Next Steps

1. **Customize content**: Add your own lessons and quizzes
2. **Configure authentication**: Set up Google OAuth
3. **Deploy to production**: Use production settings
4. **Monitor usage**: Set up analytics and logging
5. **Scale**: Configure load balancing and caching

---

**Happy Learning! 🎓**