from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.contrib.auth.models import User
from administration.models import Teacher, Department, Course, Enrollment, Attendance
from django.contrib import messages
from teachers.models import Grade
from django.db.models import Q, Count, Avg, F
from decimal import Decimal

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
    if request.method == 'POST':
        if 'add_student' in request.POST:
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
                user.profile.role = 'student'
                user.profile.save()
                messages.success(request, 'Student created successfully.')
            return redirect('admin_students')
            
        elif 'enroll_student' in request.POST:
            student_id = request.POST.get('student')
            course_id = request.POST.get('course')
            if student_id and course_id:
                student = User.objects.filter(id=student_id, profile__role='student').first()
                course = Course.objects.filter(id=course_id).first()
                if student and course:
                    if Enrollment.objects.filter(student=student, course=course).exists():
                        messages.error(request, 'Student is already enrolled in this course.')
                    else:
                        Enrollment.objects.create(student=student, course=course)
                        messages.success(request, 'Student enrolled successfully.')
            return redirect('admin_students')

    students = User.objects.filter(profile__role='student')
    courses = Course.objects.all()
    enrollments = Enrollment.objects.all().order_by('-id')
    return render(request, 'administration/students.html', {
        'students': students,
        'courses': courses,
        'enrollments': enrollments
    })

@login_required
@role_required('admin')
def admin_departments(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            if Department.objects.filter(name=name).exists():
                messages.error(request, 'Department already exists.')
            else:
                Department.objects.create(name=name)
                messages.success(request, 'Department created successfully.')
        return redirect('admin_departments')
        
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
    if request.method == 'POST':
        name = request.POST.get('name')
        department_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')

        if name and department_id:
            try:
                department = Department.objects.get(id=department_id)
                teacher = None
                if teacher_id:
                    # Make sure the user is a teacher
                    teacher = User.objects.filter(id=teacher_id, profile__role='teacher').first()
                
                Course.objects.create(
                    name=name,
                    department=department,
                    teacher=teacher
                )
                messages.success(request, 'Course created successfully.')
            except Department.DoesNotExist:
                messages.error(request, 'Selected department does not exist.')
            except Exception as e:
                messages.error(request, f'Error creating course: {str(e)}')
            
            return redirect('admin_courses')

    courses = Course.objects.all()
    departments = Department.objects.all()
    teachers = User.objects.filter(profile__role='teacher')
    
    context = {
        'courses': courses,
        'departments': departments,
        'teachers': teachers
    }
    return render(request, 'administration/courses.html', context)

@login_required
@role_required('admin')
def admin_defaulters(request):
    """
    Generate automated defaulter list based on:
    1. Attendance < 75%
    2. Average grades < 40%
    3. Multiple low grades
    """
    students = User.objects.filter(profile__role='student')
    defaulters = []
    
    for student in students:
        reasons = []
        attendance_percentage = 0
        average_grade = 0
        
        # Check attendance
        enrollments = Enrollment.objects.filter(student=student)
        for enrollment in enrollments:
            attendance_records = Attendance.objects.filter(
                student=student,
                course=enrollment.course
            )
            if attendance_records.count() > 0:
                present_count = attendance_records.filter(present=True).count()
                total_count = attendance_records.count()
                attendance_percentage = (present_count / total_count) * 100
                
                if attendance_percentage < 75:
                    reasons.append(f"Low Attendance ({attendance_percentage:.1f}%) in {enrollment.course.name}")
        
        # Check grades
        grades = Grade.objects.filter(student=student)
        if grades.exists():
            total_marks_sum = Decimal(0)
            obtained_marks_sum = Decimal(0)
            
            for grade in grades:
                obtained_marks_sum += grade.marks_obtained
                total_marks_sum += grade.total_marks
            
            if total_marks_sum > 0:
                average_grade = (obtained_marks_sum / total_marks_sum) * 100
                
                if average_grade < 40:
                    reasons.append(f"Poor Academic Performance (Average: {average_grade:.1f}%)")
        
        # Add to defaulters if has any reason
        if reasons:
            defaulters.append({
                'student': student,
                'reasons': reasons,
                'attendance': f"{attendance_percentage:.1f}%",
                'average_grade': f"{average_grade:.1f}%",
                'enrolled_courses': enrollments.count()
            })
    
    context = {
        'defaulters': defaulters,
        'total_defaulters': len(defaulters),
        'total_students': students.count(),
    }
    return render(request, 'administration/defaulters.html', context)
