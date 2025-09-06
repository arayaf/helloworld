from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProgress


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'university', 'major', 'year_of_study', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'year_of_study', 'university')
    search_fields = ('email', 'first_name', 'last_name', 'university', 'major')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_picture', 'bio')}),
        ('Academic info', {'fields': ('university', 'major', 'year_of_study')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'topic', 'completion_percentage', 'score', 'last_accessed')
    list_filter = ('subject', 'created_at', 'last_accessed')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'subject', 'topic')
    readonly_fields = ('created_at', 'last_accessed')