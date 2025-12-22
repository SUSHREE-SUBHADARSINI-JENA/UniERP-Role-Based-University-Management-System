from django.shortcuts import render
from accounts.decorators import role_required

@role_required('student')
def student_dashboard(request):
    return render(request, 'students/dashboard.html')

