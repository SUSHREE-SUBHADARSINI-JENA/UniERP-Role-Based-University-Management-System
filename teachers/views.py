from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Teacher
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def teachers_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teachers_list.html', {'teachers': teachers})


@login_required
@user_passes_test(is_admin)
def add_teacher(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email']
        )

        Teacher.objects.create(
            user=user,
            employee_id=request.POST['employee_id'],
            department=request.POST['department'],
            phone=request.POST['phone']
        )
        return redirect('teachers')

    return render(request, 'teachers/add_teacher.html')
