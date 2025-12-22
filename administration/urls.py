from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('students/', views.admin_students, name='admin_students'),
    path('teachers/', views.admin_teachers, name='admin_teachers'),
    path('departments/', views.admin_departments, name='admin_departments'),
    path('courses/', views.admin_courses, name='admin_courses'),
    path('departments/', views.admin_departments, name='admin_departments'),
    path('departments/delete/<int:dept_id>/', views.delete_department, name='delete_department'),

]

