from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Subject(models.Model):
    """STEM subjects like Mathematics, Physics, Chemistry, etc."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fas fa-book')
    color = models.CharField(max_length=7, default='#DC143C')  # Crimson color
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Topic(models.Model):
    """Topics within each subject"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    difficulty_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1,
        help_text="1=Beginner, 2=Easy, 3=Intermediate, 4=Advanced, 5=Expert"
    )
    estimated_duration = models.IntegerField(help_text="Duration in minutes")
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['subject', 'order']
        unique_together = ['subject', 'title']
    
    def __str__(self):
        return f"{self.subject.name}: {self.title}"


class Lesson(models.Model):
    """Individual lessons within topics"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    content = models.TextField()
    lesson_type = models.CharField(
        max_length=20,
        choices=[
            ('theory', 'Theory'),
            ('example', 'Example'),
            ('exercise', 'Exercise'),
            ('quiz', 'Quiz'),
        ],
        default='theory'
    )
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='lessons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['topic', 'order']
    
    def __str__(self):
        return f"{self.topic.title}: {self.title}"


class Quiz(models.Model):
    """Quiz questions for lessons"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    question = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=[
            ('multiple_choice', 'Multiple Choice'),
            ('true_false', 'True/False'),
            ('fill_blank', 'Fill in the Blank'),
            ('short_answer', 'Short Answer'),
        ],
        default='multiple_choice'
    )
    points = models.IntegerField(default=1)
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Quiz: {self.question[:50]}..."


class QuizOption(models.Model):
    """Answer options for quiz questions"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.quiz.question[:30]}... - {self.option_text}"


class UserLessonProgress(models.Model):
    """Track user progress through lessons"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)
    time_spent = models.IntegerField(default=0, help_text="Time spent in seconds")
    last_accessed = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'lesson']
    
    def __str__(self):
        return f"{self.user.full_name} - {self.lesson.title}"


class UserQuizAttempt(models.Model):
    """Track user quiz attempts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    selected_option = models.ForeignKey(QuizOption, on_delete=models.CASCADE, null=True, blank=True)
    answer_text = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.full_name} - {self.quiz.question[:30]}..."


class Formula(models.Model):
    """Mathematical and scientific formulas"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='formulas')
    name = models.CharField(max_length=100)
    formula_text = models.CharField(max_length=200)
    description = models.TextField()
    variables = models.JSONField(default=dict, help_text="Variable definitions")
    example_usage = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subject.name}: {self.name}"


class StudyGroup(models.Model):
    """Study groups for collaborative learning"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='study_groups')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_study_groups')
    members = models.ManyToManyField(User, related_name='study_groups', blank=True)
    is_public = models.BooleanField(default=True)
    max_members = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.subject.name})"
    
    @property
    def member_count(self):
        return self.members.count()