from django.urls import path
from .views import teacher_dashboard
from .views import mark_attendance
from . import views

urlpatterns = [
    path('dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('attendance/', mark_attendance, name='mark_attendance'),
    path('', views.teachers_list, name='teachers'),
    path('add/', views.add_teacher, name='add_teacher'),
    path('edit/<int:id>/', views.edit_teacher, name='edit_teacher'),
    path('delete/<int:id>/', views.delete_teacher, name='delete_teacher'),
]
