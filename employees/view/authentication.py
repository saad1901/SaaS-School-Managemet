from django.shortcuts import render
from employees.models import Users
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import *
from django.http import JsonResponse
from django.contrib.auth import logout

from django.contrib import messages
@login_required
@user_passes_test(allusers)
def logoutuser(request):
    print(1)
    logout(request)
    return redirect('login_view')