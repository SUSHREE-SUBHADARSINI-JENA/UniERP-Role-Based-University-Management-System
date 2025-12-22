from django.contrib import admin
from django.urls import path, include
from accounts.views import dashboard_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('dashboard/', dashboard_redirect, name='dashboard'),

    path('administration/', include('administration.urls')),
    path('teachers/', include('teachers.urls')),
    path('students/', include('students.urls')),
]
