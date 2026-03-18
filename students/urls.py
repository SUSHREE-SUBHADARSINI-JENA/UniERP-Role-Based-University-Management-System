from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('courses/', views.student_courses, name='student_courses'),
    path('assignments/', views.student_assignments, name='student_assignments'),
    path('attendance/', views.student_attendance, name='student_attendance'),
    path('grades/', views.student_grades, name='student_grades'),
    path('materials/', views.student_materials, name='student_materials'),
]
