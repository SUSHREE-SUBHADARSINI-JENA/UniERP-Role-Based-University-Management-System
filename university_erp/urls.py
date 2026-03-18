from django.contrib import admin
from django.urls import path, include
from accounts.views import dashboard_redirect
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('dashboard/', dashboard_redirect, name='dashboard'),

    path('administration/', include('administration.urls')),
    path('teachers/', include('teachers.urls')),
    path('students/', include('students.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
