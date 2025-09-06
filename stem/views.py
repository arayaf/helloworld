from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
from .models import (
    Subject, Topic, Lesson, Quiz, QuizOption, 
    UserLessonProgress, UserQuizAttempt, Formula, StudyGroup
)
from .forms import StudyGroupForm, QuizSubmissionForm


class SubjectListView(ListView):
    model = Subject
    template_name = 'stem/subject_list.html'
    context_object_name = 'subjects'


class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'stem/subject_detail.html'
    context_object_name = 'subject'


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'stem/topic_detail.html'
    context_object_name = 'topic'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Get user progress for lessons in this topic
            lessons = self.object.lessons.all()
            progress_data = []
            for lesson in lessons:
                try:
                    progress = UserLessonProgress.objects.get(
                        user=self.request.user, 
                        lesson=lesson
                    )
                    progress_data.append({
                        'lesson': lesson,
                        'progress': progress,
                        'completed': progress.completed
                    })
                except UserLessonProgress.DoesNotExist:
                    progress_data.append({
                        'lesson': lesson,
                        'progress': None,
                        'completed': False
                    })
            context['lesson_progress'] = progress_data
        return context


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'stem/lesson_detail.html'
    context_object_name = 'lesson'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get or create user progress
        progress, created = UserLessonProgress.objects.get_or_create(
            user=self.request.user,
            lesson=self.object
        )
        context['user_progress'] = progress
        
        # Get quizzes for this lesson
        context['quizzes'] = self.object.quizzes.all()
        
        return context


class CompleteLessonView(LoginRequiredMixin, DetailView):
    model = Lesson
    
    def post(self, request, *args, **kwargs):
        lesson = self.get_object()
        progress, created = UserLessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )
        
        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()
            
            # Update user's overall progress
            from users.models import UserProgress
            user_progress, created = UserProgress.objects.get_or_create(
                user=request.user,
                subject=lesson.topic.subject.name,
                topic=lesson.topic.title,
                defaults={'total_lessons': 0}
            )
            user_progress.completed_lessons += 1
            user_progress.save()
            
            messages.success(request, f'Congratulations! You completed "{lesson.title}"')
        
        return redirect('stem:lesson_detail', pk=lesson.pk)


class QuizView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'stem/quiz.html'
    context_object_name = 'quiz'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuizSubmissionForm(quiz=self.object)
        return context


class SubmitQuizView(LoginRequiredMixin, DetailView):
    model = Quiz
    
    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        form = QuizSubmissionForm(request.POST, quiz=quiz)
        
        if form.is_valid():
            selected_option_id = form.cleaned_data.get('selected_option')
            answer_text = form.cleaned_data.get('answer_text', '')
            
            # Get the selected option
            selected_option = None
            if selected_option_id:
                try:
                    selected_option = QuizOption.objects.get(id=selected_option_id)
                except QuizOption.DoesNotExist:
                    pass
            
            # Determine if answer is correct
            is_correct = False
            points_earned = 0
            
            if quiz.question_type == 'multiple_choice':
                is_correct = selected_option and selected_option.is_correct
                points_earned = quiz.points if is_correct else 0
            elif quiz.question_type == 'true_false':
                is_correct = selected_option and selected_option.is_correct
                points_earned = quiz.points if is_correct else 0
            elif quiz.question_type in ['fill_blank', 'short_answer']:
                # For text answers, we'll need to implement more sophisticated checking
                # For now, we'll give partial credit
                is_correct = bool(answer_text.strip())
                points_earned = quiz.points if is_correct else 0
            
            # Create quiz attempt
            attempt = UserQuizAttempt.objects.create(
                user=request.user,
                quiz=quiz,
                selected_option=selected_option,
                answer_text=answer_text,
                is_correct=is_correct,
                points_earned=points_earned
            )
            
            # Update lesson progress
            lesson = quiz.lesson
            progress, created = UserLessonProgress.objects.get_or_create(
                user=request.user,
                lesson=lesson
            )
            
            # Update score based on quiz performance
            if is_correct:
                progress.score = max(progress.score, points_earned)
                progress.save()
            
            return JsonResponse({
                'success': True,
                'is_correct': is_correct,
                'points_earned': points_earned,
                'explanation': quiz.explanation,
                'correct_option': selected_option.option_text if selected_option and selected_option.is_correct else None
            })
        
        return JsonResponse({'success': False, 'errors': form.errors})


class FormulaListView(ListView):
    model = Formula
    template_name = 'stem/formula_list.html'
    context_object_name = 'formulas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        subject_id = self.request.GET.get('subject')
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        return context


class FormulaDetailView(DetailView):
    model = Formula
    template_name = 'stem/formula_detail.html'
    context_object_name = 'formula'


class StudyGroupListView(ListView):
    model = StudyGroup
    template_name = 'stem/study_group_list.html'
    context_object_name = 'study_groups'
    paginate_by = 10
    
    def get_queryset(self):
        return StudyGroup.objects.filter(is_public=True).order_by('-created_at')


class StudyGroupDetailView(DetailView):
    model = StudyGroup
    template_name = 'stem/study_group_detail.html'
    context_object_name = 'study_group'


class JoinStudyGroupView(LoginRequiredMixin, DetailView):
    model = StudyGroup
    
    def post(self, request, *args, **kwargs):
        study_group = self.get_object()
        
        if study_group.member_count < study_group.max_members:
            if request.user not in study_group.members.all():
                study_group.members.add(request.user)
                messages.success(request, f'You joined "{study_group.name}"!')
            else:
                messages.info(request, 'You are already a member of this study group.')
        else:
            messages.error(request, 'This study group is full.')
        
        return redirect('stem:study_group_detail', pk=study_group.pk)


class CreateStudyGroupView(LoginRequiredMixin, CreateView):
    model = StudyGroup
    form_class = StudyGroupForm
    template_name = 'stem/create_study_group.html'
    success_url = reverse_lazy('stem:study_group_list')
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, 'Study group created successfully!')
        return super().form_valid(form)