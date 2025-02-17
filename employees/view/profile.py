from django.shortcuts import render
from employees.models import Users
from employees.forms import UserProfileForm
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib import messages

@login_required
@user_passes_test(allusers)
def profile(request):
    return render(request, 'employees/profile/profile.html')

@login_required
@user_passes_test(mangagement)
def profile_edit_admin(request, id):
    user = Users.objects.get(id=id)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('employees')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'employees/profile/profile_edit.html', {'form': form, 'id':id})

@login_required
@user_passes_test(allusers)
def profile_edit(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'employees/profile/profile_edit.html', {'form': form,'id':user.id, 'personal': True})

@login_required
@user_passes_test(allusers)
def credentials(request, id):
    if not mangagement(request.user) and request.user.id is not id:
        # return JsonResponse({'message': 'Unauthorized Acess !'}, status=500)
        id = request.user.id
        
    user = Users.objects.get(id=id)
    print('I was not called')
    if request.method == 'POST':
        password = request.POST.get('password')

        # Validate password length and complexity (Optional)
        if len(password) < 8 or not any(char.isdigit() for char in password) \
           or not any(char.islower() for char in password) \
           or not any(char.isupper() for char in password):
            messages.error(request, "Password must contain at least 8 characters, one uppercase, one lowercase, and one number.")
            return render(request, 'employees/profile/credentials.html')

        user.password = make_password(password)
        user.hint = password
        user.save()
        if id == request.user.id:
            login(request, user)
        messages.success(request, "password has been successfully updated!")
        print(user.id, id)
    return render(request, 'employees/profile/credentials.html', {'user2':user,'id': id})
