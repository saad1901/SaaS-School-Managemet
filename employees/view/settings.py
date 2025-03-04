from django.shortcuts import render
from employees.models import SchoolInfo, Users
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


@login_required
@user_passes_test(superadmin)
def storagemanage(request):
    users = Users.objects.all().values("id", "name", "storage", "max_storage")
    for user in users:
        user["available_storage"] = user["max_storage"] - user["storage"]

    return render(request, 'employees/settings/storagemanage.html', {'users': users})