from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from administration.models import Course, Enrollment, Attendance
from teachers.models import Assignment, QuestionPaper, Grade

@login_required
@role_required('student')
def student_dashboard(request):
    user = request.user
    enrolled_courses = Enrollment.objects.filter(student=user)
    courses = [enrollment.course for enrollment in enrolled_courses]
    total_courses = enrolled_courses.count()
    
    recent_assignments = Assignment.objects.filter(course__in=courses).order_by('-due_date')[:5]
    recent_grades = Grade.objects.filter(student=user).order_by('-id')[:5]
    
    total_attendance_records = Attendance.objects.filter(student=user).count()
    present_records = Attendance.objects.filter(student=user, present=True).count()
    attendance_percentage = (present_records / total_attendance_records * 100) if total_attendance_records > 0 else 0
    
    context = {
        'total_courses': total_courses,
        'recent_assignments': recent_assignments,
        'recent_grades': recent_grades,
        'attendance_percentage': round(attendance_percentage, 1),
    }
    return render(request, 'students/dashboard.html', context)

@login_required
@role_required('student')
def student_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course', 'course__department', 'course__teacher')
    return render(request, 'students/courses.html', {'enrollments': enrollments})

@login_required
@role_required('student')
def student_assignments(request):
    courses = Course.objects.filter(enrollment__student=request.user)
    assignments = Assignment.objects.filter(course__in=courses).order_by('due_date')
    return render(request, 'students/assignments.html', {'assignments': assignments})

@login_required
@role_required('student')
def student_attendance(request):
    records = Attendance.objects.filter(student=request.user).select_related('course').order_by('-date')
    return render(request, 'students/attendance.html', {'records': records})

@login_required
@role_required('student')
def student_grades(request):
    grades = Grade.objects.filter(student=request.user).select_related('course').order_by('-id')
    return render(request, 'students/grades.html', {'grades': grades})

@login_required
@role_required('student')
def student_materials(request):
    courses = Course.objects.filter(enrollment__student=request.user)
    materials = QuestionPaper.objects.filter(course__in=courses).select_related('course').order_by('-uploaded_at')
    return render(request, 'students/materials.html', {'materials': materials})
