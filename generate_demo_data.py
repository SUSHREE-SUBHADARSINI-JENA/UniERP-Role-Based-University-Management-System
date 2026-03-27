import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_erp.settings')
django.setup()

from django.contrib.auth.models import User, Group
from administration.models import Department, Course, Enrollment

def create_demo_data():
    print("Creating Roles/Groups...")
    admin_group, _ = Group.objects.get_or_create(name='Administrator')
    teacher_group, _ = Group.objects.get_or_create(name='Teacher')
    student_group, _ = Group.objects.get_or_create(name='Student')

    print("Creating Demo Users...")
    
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin_user.groups.add(admin_group)
        admin_user.profile.role = 'admin'
        admin_user.profile.save()
    
    if not User.objects.filter(username='teacher_demo').exists():
        teacher_user = User.objects.create_user('teacher_demo', 'teacher@example.com', 'teacher123')
        teacher_user.groups.add(teacher_group)
        teacher_user.profile.role = 'teacher'
        teacher_user.profile.save()
    else:
        teacher_user = User.objects.get(username='teacher_demo')
        
    if not User.objects.filter(username='student_demo').exists():
        student_user = User.objects.create_user('student_demo', 'student@example.com', 'student123')
        student_user.groups.add(student_group)
        student_user.profile.role = 'student'
        student_user.profile.save()
    else:
        student_user = User.objects.get(username='student_demo')

    print("Creating Departments...")
    dept_cs, _ = Department.objects.get_or_create(name="Computer Science")
    dept_math, _ = Department.objects.get_or_create(name="Mathematics")

    print("Creating Courses...")
    course1, _ = Course.objects.get_or_create(
        name="Introduction to Computer Science",
        defaults={
            'department': dept_cs,
            'teacher': teacher_user
        }
    )
    course2, _ = Course.objects.get_or_create(
        name="Calculus I",
        defaults={
            'department': dept_math,
            'teacher': teacher_user
        }
    )

    print("Creating Enrollments...")
    Enrollment.objects.get_or_create(student=student_user, course=course1)
    Enrollment.objects.get_or_create(student=student_user, course=course2)

    print("Demo Data Generation Completed Successfully!")

if __name__ == '__main__':
    create_demo_data()
