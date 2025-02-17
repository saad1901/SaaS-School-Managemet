from django.shortcuts import render
# from employees.models import 
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import allusers

@login_required
@user_passes_test(allusers)
def students(request):
    return render(request, 'employees/students/students.html')