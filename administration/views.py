from django.shortcuts import render
from accounts.decorators import role_required
from django.shortcuts import redirect

@role_required('admin')
def admin_dashboard(request):
    return render(request, 'administration/dashboard.html')

@role_required('admin')
def admin_students(request):
    return render(request, 'administration/students.html')

@role_required('admin')
def admin_teachers(request):
    return render(request, 'administration/teachers.html')

@role_required('admin')
def admin_departments(request):
    return render(request, 'administration/departments.html')

@role_required('admin')
def admin_courses(request):
    return render(request, 'administration/courses.html')
from .models import Department

@role_required('admin')
def admin_departments(request):
    departments = Department.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Department.objects.create(name=name)

    return render(
        request,
        'administration/departments.html',
        {'departments': departments}
    )


@role_required('admin')
def delete_department(request, dept_id):
    Department.objects.filter(id=dept_id).delete()
    return redirect('admin_departments')