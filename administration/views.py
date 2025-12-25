from django.shortcuts import render
from accounts.decorators import role_required
from django.shortcuts import redirect
from .models import Department
from .models import Course, Department
from django.contrib.auth.models import User
from .models import Enrollment

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



@role_required('admin')
def admin_courses(request):
    courses = Course.objects.select_related('department', 'teacher')
    departments = Department.objects.all()
    teachers = User.objects.filter(profile__role='teacher')

    if request.method == 'POST':
        name = request.POST.get('name')
        dept_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')

        if name and dept_id:
            Course.objects.create(
                name=name,
                department_id=dept_id,
                teacher_id=teacher_id if teacher_id else None
            )

    return render(
        request,
        'administration/courses.html',
        {
            'courses': courses,
            'departments': departments,
            'teachers': teachers
        }
    )



@role_required('admin')
def admin_students(request):
    students = User.objects.filter(profile__role='student')
    courses = Course.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')

        if student_id and course_id:
            Enrollment.objects.get_or_create(
                student_id=student_id,
                course_id=course_id
            )

    enrollments = Enrollment.objects.select_related('student', 'course')

    return render(
        request,
        'administration/students.html',
        {
            'students': students,
            'courses': courses,
            'enrollments': enrollments
        }
    )