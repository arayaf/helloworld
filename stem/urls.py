from django.urls import path
from . import views

app_name = 'stem'

urlpatterns = [
    path('', views.SubjectListView.as_view(), name='subject_list'),
    path('subject/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('lesson/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/<int:pk>/complete/', views.CompleteLessonView.as_view(), name='complete_lesson'),
    path('quiz/<int:pk>/', views.QuizView.as_view(), name='quiz'),
    path('quiz/<int:pk>/submit/', views.SubmitQuizView.as_view(), name='submit_quiz'),
    path('formulas/', views.FormulaListView.as_view(), name='formula_list'),
    path('formulas/<int:pk>/', views.FormulaDetailView.as_view(), name='formula_detail'),
    path('study-groups/', views.StudyGroupListView.as_view(), name='study_group_list'),
    path('study-groups/<int:pk>/', views.StudyGroupDetailView.as_view(), name='study_group_detail'),
    path('study-groups/<int:pk>/join/', views.JoinStudyGroupView.as_view(), name='join_study_group'),
    path('study-groups/create/', views.CreateStudyGroupView.as_view(), name='create_study_group'),
]