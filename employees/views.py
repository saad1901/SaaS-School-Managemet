from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password


@user_passes_test(allusers)
def logoutuser(request):
    print(1)
    logout(request)
    return redirect('login_view')


def home(request):
    return render(request, 'employees/base.html')


@user_passes_test(allusers)
def dashboard(request):
    return render(request, 'employees/dashboard.html')


@user_passes_test(allusers)
def admincloud(request, uid):
    user = request.user
    files = Files.objects.filter(parent=uid, fk=user.id)
    message = None
    message_type = None

    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        if folder_name:
            if not Files.objects.filter(name=folder_name, ftype='folder', parent=uid, fk=request.user).exists():
                Files.objects.create(name=folder_name, ftype='folder', fk=user, parent=uid)
                message = 'Folder created successfully!'
                message_type = 'success'
            else:
                message = 'Folder already exists or invalid data provided.'
                message_type = 'error'
                return render(request, 'employees/cloud.html', 
                            {'context': files, 'uid': uid, 'message': message, 'message_type': message_type})

    return render(request, 'employees/cloud.html', 
                {'context': files, 'uid': uid, 'message': message, 'message_type': message_type})

@user_passes_test(allusers)
def teachers(request):
    employees = Users.objects.all()
    return render(request, 'employees/teachers.html' ,{'employees':employees})

def generate_password():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    

@user_passes_test(superadmin)
def addteacher(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        date_of_joining = request.POST.get("date_of_joining")
        role = request.POST.get("role")
        salary = request.POST.get("salary") or None
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal_code = request.POST.get("postal_code")
        password = generate_password()
        print(password)
        hashed_password = make_password(password)
        Users.objects.create(
            name=name, email=email, phone=phone, dob=dob, gender=gender,
            date_of_joining=date_of_joining, role=role, salary=salary,
            address=address, city=city, state=state, postal_code=postal_code, password=hashed_password, hint=password
        )

        return redirect("teachers")

    return render(request, 'employees/addteacher.html')

@user_passes_test(allusers)
@csrf_exempt
def ajax_file_upload(request, dir_id=None):
    if request.method == 'POST' and request.FILES.get('file'):
        file_obj = request.FILES['file']
        file_name = file_obj.name
        file_type = file_obj.content_type.split('/')[1]
        parent_dir = str(dir_id) if dir_id is not None else '' 

        # Check if a file with the same name and type exists in the parent directory
        if Files.objects.filter(name=file_name, ftype=file_type, parent=parent_dir, fk=request.user).exists():
            print('existerror')
            return JsonResponse({
                'message': 'This file already exists in the specified directory.'
            }, status=400)

        # Save the file to the database
        file_instance = Files.objects.create(
            name=file_name,
            ftype=file_type,
            file=file_obj,
            fk=request.user, 
            parent=parent_dir
        )

        return JsonResponse({
            'message': 'File uploaded successfully',
            'file_url': file_instance.file.url
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)
