from django.shortcuts import render
from employees.models import Class

def classes(request):
    classes = Class.objects.all()
    return render(request, 'employees/class/classes.html', {'classes':classes})