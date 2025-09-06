from django.contrib import admin
from .models import (
    Subject, Topic, Lesson, Quiz, QuizOption, 
    UserLessonProgress, UserQuizAttempt, Formula, StudyGroup
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'difficulty_level', 'estimated_duration', 'order')
    list_filter = ('subject', 'difficulty_level')
    search_fields = ('title', 'description')
    ordering = ('subject', 'order')


class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 4


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'lesson', 'question_type', 'points')
    list_filter = ('question_type', 'lesson__topic__subject')
    search_fields = ('question', 'lesson__title')
    inlines = [QuizOptionInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'lesson_type', 'order')
    list_filter = ('lesson_type', 'topic__subject')
    search_fields = ('title', 'content')
    ordering = ('topic', 'order')


@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'score', 'time_spent', 'last_accessed')
    list_filter = ('completed', 'lesson__topic__subject', 'last_accessed')
    search_fields = ('user__email', 'user__first_name', 'lesson__title')
    readonly_fields = ('last_accessed',)


@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'is_correct', 'points_earned', 'attempted_at')
    list_filter = ('is_correct', 'quiz__lesson__topic__subject', 'attempted_at')
    search_fields = ('user__email', 'quiz__question')
    readonly_fields = ('attempted_at',)


@admin.register(Formula)
class FormulaAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'formula_text')
    list_filter = ('subject',)
    search_fields = ('name', 'formula_text', 'description')


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'creator', 'member_count', 'is_public', 'created_at')
    list_filter = ('subject', 'is_public', 'created_at')
    search_fields = ('name', 'description', 'creator__email')
    filter_horizontal = ('members',)