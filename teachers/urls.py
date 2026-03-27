from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('attendance/', views.mark_attendance, name='mark_attendance'),
    path('assignments/', views.manage_assignments, name='manage_assignments'),
    path('grades/', views.manage_grades, name='manage_grades'),
    path('questions/', views.manage_questions, name='manage_questions'),
]
