from django.shortcuts import render
from employees.models import SchoolInfo
from employees.forms import SchoolInfoForm
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import allusers, superadmin

@login_required
@user_passes_test(allusers)
def settings(request):
    user = request.user
    info = SchoolInfo.objects.first()
    if request.method == 'POST':
        form = SchoolInfoForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
    else:
        form = SchoolInfoForm(instance=info)
    return render(request,  'employees/settings/settings.html', {'form':form})

@login_required
@user_passes_test(superadmin)
def addrole(request):
    return render(request, 'employees/settings/addrole.html')


@login_required
@user_passes_test(superadmin)
def settingspermissions(request):
    return render(request, 'employees/settings/permissions.html')