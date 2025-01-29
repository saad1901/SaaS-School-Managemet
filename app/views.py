from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def allusers(user):
    if user.role == 'Teacher' or user.role == 'Super Admin':
        return True

def superadmin(user):
    if user.role == 'Super Admin':
        return True

def login_view(request):
    if request.method == 'POST':
        # Get the data from the form
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print(email)
        print(password)
        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            print(1)
            login(request, user)
            # Redirect to the dashboard page
            return redirect('teachercloud', uid=0)  # Replace 'dashboard' with the actual URL or view name
        else:
            print(2)
            messages.error(request, "Invalid credentials, please try again.")
    
    return render(request, 'landings/loginpage.html')
