from django.shortcuts import render
# from employees.models import
# from employees.forms import 
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import allusers

@login_required
@user_passes_test(allusers)
def home(request):
    # info  = SchoolInfo.objects.first()
    return render(request, 'employees/base/base.html')