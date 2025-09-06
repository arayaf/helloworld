from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    university = models.CharField(max_length=100, blank=True)
    major = models.CharField(max_length=100, blank=True)
    year_of_study = models.IntegerField(default=1)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserProgress(models.Model):
    """Track user's learning progress"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_set')
    subject = models.CharField(max_length=50)
    topic = models.CharField(max_length=100)
    completed_lessons = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    score = models.FloatField(default=0.0)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'subject', 'topic']
    
    def __str__(self):
        return f"{self.user.full_name} - {self.subject}: {self.topic}"
    
    @property
    def completion_percentage(self):
        if self.total_lessons == 0:
            return 0
        return (self.completed_lessons / self.total_lessons) * 100