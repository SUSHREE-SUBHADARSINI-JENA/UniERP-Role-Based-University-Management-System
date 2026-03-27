from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.contrib.auth.models import User
from administration.models import Teacher, Department, Course
from django.contrib import messages

@login_required
@role_required('admin')
def admin_dashboard(request):
    context = {
        'total_students': User.objects.filter(profile__role='student').count(),
        'total_teachers': User.objects.filter(profile__role='teacher').count(),
        'total_departments': Department.objects.count(),
        'total_courses': Course.objects.count(),
    }
    return render(request, 'administration/dashboard.html', context)

@login_required
@role_required('admin')
def admin_teachers(request):
    if request.method == 'POST' and 'add_teacher' in request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.profile.role = 'teacher'
            user.profile.save()
            messages.success(request, 'Teacher created successfully.')
            return redirect('admin_teachers')

    teachers = User.objects.filter(profile__role='teacher')
    return render(request, 'administration/teachers.html', {'teachers': teachers})

@login_required
@role_required('admin')
def admin_students(request):
    students = User.objects.filter(profile__role='student')
    return render(request, 'administration/students.html', {'students': students})

@login_required
@role_required('admin')
def admin_departments(request):
    departments = Department.objects.all()
    return render(request, 'administration/departments.html', {'departments': departments})

@login_required
@role_required('admin')
def delete_department(request, dept_id):
    dept = get_object_or_404(Department, id=dept_id)
    dept.delete()
    messages.success(request, 'Department deleted successfully.')
    return redirect('admin_departments')

@login_required
@role_required('admin')
def admin_courses(request):
    courses = Course.objects.all()
    return render(request, 'administration/courses.html', {'courses': courses})
