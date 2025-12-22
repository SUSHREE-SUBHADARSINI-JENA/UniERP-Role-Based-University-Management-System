from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required
def dashboard_redirect(request):
    role = request.user.profile.role

    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'teacher':
        return redirect('teacher_dashboard')
    elif role == 'student':
        return redirect('student_dashboard')

    return redirect('login')
