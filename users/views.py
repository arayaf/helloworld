from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import User, UserProgress
from .forms import ProfileEditForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_progress'] = UserProgress.objects.filter(user=self.request.user)
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)


class ProgressView(LoginRequiredMixin, TemplateView):
    template_name = 'users/progress.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        progress = UserProgress.objects.filter(user=self.request.user)
        
        # Group progress by subject
        subjects = {}
        for p in progress:
            if p.subject not in subjects:
                subjects[p.subject] = []
            subjects[p.subject].append(p)
        
        context['subjects'] = subjects
        context['total_progress'] = progress
        return context