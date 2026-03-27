from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.contrib import messages
from django.contrib.auth.models import User
from administration.models import Course, Attendance
from .models import Assignment, Grade, QuestionPaper

@login_required
@role_required('teacher')
def teacher_dashboard(request):
    courses = Course.objects.filter(teacher=request.user)
    
    total_students = User.objects.filter(profile__role='student').count()
    total_assignments = Assignment.objects.filter(course__in=courses).count()
    total_materials = QuestionPaper.objects.filter(course__in=courses).count()

    context = {
        'courses': courses,
        'total_students': total_students,
        'total_assignments': total_assignments,
        'total_materials': total_materials
    }
    return render(request, 'teachers/dashboard.html', context)

@login_required
@role_required('teacher')
def mark_attendance(request):
    courses = Course.objects.filter(teacher=request.user)
    
    selected_course_id = request.GET.get('course')
    students = None
    if selected_course_id:
        from administration.models import Enrollment
        enrollments = Enrollment.objects.filter(course_id=selected_course_id)
        students = [e.student for e in enrollments]

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        date = request.POST.get('date')

        if course_id and date:
            course = Course.objects.get(id=course_id)
            from administration.models import Enrollment
            enrollments = Enrollment.objects.filter(course=course)
            enrolled_students = [e.student for e in enrollments]
            for student in enrolled_students:
                # checkbox only sends 'on' if checked (name="student_<id>")
                status = request.POST.get(f'student_{student.id}')
                is_present = (status == 'on')
                Attendance.objects.update_or_create(
                    student=student,
                    course=course,
                    date=date,
                    defaults={'present': is_present}
                )
            messages.success(request, 'Attendance marked successfully.')        
            return redirect('mark_attendance')

    return render(request, 'teachers/attendance.html', {
        'courses': courses,
        'students': students,
        'selected_course': selected_course_id
    })

@login_required
@role_required('teacher')
def manage_assignments(request):
    courses = Course.objects.filter(teacher=request.user)
    assignments = Assignment.objects.filter(course__in=courses).order_by('-created_at')
    
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        
        if course_id and title and due_date:
            course = Course.objects.get(id=course_id)
            Assignment.objects.create(
                course=course,
                title=title,
                description=description,
                due_date=due_date
            )
            messages.success(request, 'Assignment added successfully.')
            return redirect('manage_assignments')

    return render(request, 'teachers/assignments.html', {
        'courses': courses,
        'assignments': assignments
    })

@login_required
@role_required('teacher')
def manage_grades(request):
    courses = Course.objects.filter(teacher=request.user)
    grades = Grade.objects.filter(course__in=courses).order_by('course', 'exam_name', 'student__username')

    selected_course_id = request.GET.get('course')
    students = None
    if selected_course_id:
        from administration.models import Enrollment
        enrollments = Enrollment.objects.filter(course_id=selected_course_id)
        students = [e.student for e in enrollments]

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        student_id = request.POST.get('student_id')
        exam_name = request.POST.get('exam_name')
        marks_obtained = request.POST.get('marks_obtained')
        total_marks = request.POST.get('total_marks')

        if course_id and student_id and exam_name and marks_obtained and total_marks:
            course = Course.objects.get(id=course_id)
            student = User.objects.get(id=student_id)
            Grade.objects.create(
                course=course,
                student=student,
                exam_name=exam_name,
                marks_obtained=marks_obtained,
                total_marks=total_marks
            )
            messages.success(request, 'Grade added successfully.')
            return redirect(f'/teachers/grades/?course={course_id}')

    return render(request, 'teachers/grades.html', {
        'courses': courses,
        'students': students,
        'grades': grades,
        'selected_course': selected_course_id
    })

@login_required
@role_required('teacher')
def manage_questions(request):
    courses = Course.objects.filter(teacher=request.user)
    materials = QuestionPaper.objects.filter(course__in=courses).order_by('-uploaded_at')
    
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        title = request.POST.get('title')
        file = request.FILES.get('file')
        
        if course_id and title and file:
            course = Course.objects.get(id=course_id)
            QuestionPaper.objects.create(
                course=course,
                title=title,
                file=file
            )
            messages.success(request, 'Material uploaded successfully.')
            return redirect('manage_questions')

    return render(request, 'teachers/questions.html', {
        'courses': courses,
        'materials': materials
    })
