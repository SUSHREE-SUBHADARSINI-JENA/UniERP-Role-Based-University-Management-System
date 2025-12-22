from django.shortcuts import render
from accounts.decorators import role_required

@role_required('teacher')
def teacher_dashboard(request):
    return render(request, 'teachers/dashboard.html')
