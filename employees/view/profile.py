from django.shortcuts import render
from employees.models import *
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password


@login_required
@user_passes_test(allusers)
def profile(request):
    return render(request, 'employees/profile/profile.html')