from django.urls import path
from . import views

urlpatterns = [
    # path('login/', views.login_view, name='login'), # No login_view defined
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('no_permission/', views.no_permission, name='no_permission'),
]
