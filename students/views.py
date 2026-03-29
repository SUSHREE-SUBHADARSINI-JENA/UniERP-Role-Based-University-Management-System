from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from administration.models import Course, Enrollment, Attendance
from teachers.models import Assignment, QuestionPaper, Grade
from .sgpa_utils import calculate_course_performance, calculate_sgpa

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
    
    # Calculate SGPA
    all_grades = Grade.objects.filter(student=user)
    sgpa_data = calculate_sgpa(all_grades)
    
    context = {
        'total_courses': total_courses,
        'recent_assignments': recent_assignments,
        'recent_grades': recent_grades,
        'attendance_percentage': round(attendance_percentage, 1),
        'sgpa': sgpa_data['sgpa'],
        'sgpa_interpretation': sgpa_data['interpretation'],
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
    
    # Calculate SGPA and course performance data
    grade_details = []
    for grade in grades:
        performance = calculate_course_performance(grade.marks_obtained, grade.total_marks)
        grade_details.append({
            'grade': grade,
            'percentage': performance['percentage'],
            'grade': performance['grade'],
            'grade_point': performance['grade_point'],
        })
    
    # Calculate overall SGPA
    sgpa_data = calculate_sgpa(grades)
    
    context = {
        'grades': grades,
        'grade_details': grade_details,
        'sgpa': sgpa_data['sgpa'],
        'total_courses': sgpa_data['grade_count'],
        'sgpa_interpretation': sgpa_data['interpretation'],
    }
    return render(request, 'students/grades.html', context)

@login_required
@role_required('student')
def student_materials(request):
    courses = Course.objects.filter(enrollment__student=request.user)
    materials = QuestionPaper.objects.filter(course__in=courses).select_related('course').order_by('-uploaded_at')
    return render(request, 'students/materials.html', {'materials': materials})

@login_required
@role_required('student')
def student_sgpa_report(request):
    """Detailed SGPA and academic performance report"""
    student = request.user
    
    # Get all grades
    all_grades = Grade.objects.filter(student=student).select_related('course')
    
    # Calculate detailed performance data
    grade_report = []
    total_weighted_points = 0
    total_credits = 0
    
    for grade in all_grades:
        performance = calculate_course_performance(grade.marks_obtained, grade.total_marks)
        credit_hours = 3  # Default credit hours per course
        
        grade_report.append({
            'course': grade.course,
            'exam_name': grade.exam_name,
            'marks_obtained': grade.marks_obtained,
            'total_marks': grade.total_marks,
            'percentage': performance['percentage'],
            'letter_grade': performance['grade'],
            'grade_point': performance['grade_point'],
            'credit_hours': credit_hours,
            'course_points': performance['grade_point'] * credit_hours,
        })
        
        total_weighted_points += (performance['grade_point'] * credit_hours)
        total_credits += credit_hours
    
    # Calculate SGPA
    sgpa_data = calculate_sgpa(all_grades)
    
    # Calculate statistics
    grades_by_course = {}
    for grade in all_grades:
        course_name = grade.course.name
        if course_name not in grades_by_course:
            grades_by_course[course_name] = []
        grades_by_course[course_name].append(grade)
    
    context = {
        'student_name': student.get_full_name() or student.username,
        'grade_report': grade_report,
        'sgpa': sgpa_data['sgpa'],
        'total_courses': sgpa_data['grade_count'],
        'total_credits': sgpa_data['total_credits'],
        'sgpa_interpretation': sgpa_data['interpretation'],
        'grades_by_course': grades_by_course,
    }
    return render(request, 'students/sgpa_report.html', context)
