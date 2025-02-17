from django.shortcuts import render
from employees.models import Class, Roles, Users
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import allusers

@login_required
@user_passes_test(allusers)
def dashboard(request):
    classes = []
    if request.user.role == 'Teacher':
        classes = Class.objects.filter(monitor=request.user)
    roles = Roles.objects.exclude(name = "Super Admin")
    total_classes = Class.objects.all().count()
    role_counts = {role.name: Users.objects.filter(role=role.name).count() for role in roles}

    return render(request, 'employees/dashboard/dashboard.html', {'classes':classes,'roles':roles, 'role_counts':role_counts, 'total_classes':total_classes})
