from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from .forms import UserProfileForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage

@user_passes_test(allusers)
def profile(request):
    return render(request, 'employees/profile.html')

@user_passes_test(allusers)
def credentials(request):
    if request.method == 'POST':
        password = request.POST.get('password')

        # Validate password length and complexity (Optional)
        if len(password) < 8 or not any(char.isdigit() for char in password) \
           or not any(char.islower() for char in password) \
           or not any(char.isupper() for char in password):
            messages.error(request, "Password must contain at least 8 characters, one uppercase, one lowercase, and one number.")
            return render(request, 'employees/credentials.html')

        request.user.password = make_password(password)
        request.user.hint = password
        request.user.save()
        login(request, request.user)
        messages.success(request, "Your password has been successfully updated!")

    return render(request, 'employees/credentials.html')


@user_passes_test(allusers)
def profile_edit(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'employees/profile_edit.html', {'form': form,'id':user.id})

@user_passes_test(superadmin)
def profile_edit_admin(request, id):
    user = Users.objects.get(id=id)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('employees')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'employees/profile_edit.html', {'form': form, 'id':id})




@user_passes_test(allusers)
def logoutuser(request):
    print(1)
    logout(request)
    return redirect('login_view')


def home(request):
    return render(request, 'employees/base.html')


@user_passes_test(allusers)
def dashboard(request):
    classes = []
    if request.user.role == 'Teacher':
        # return render(request, 'employees/superadmin_dashboard.html')
        classes = Class.objects.filter(monitor=request.user)
    return render(request, 'employees/dashboard.html', {'classes': classes})


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
                return render(request, 'employees/cloudtest.html', 
                            {'context': files, 'uid': uid, 'message': message, 'message_type': message_type})

    return render(request, 'employees/cloudtest.html', 
                {'context': files, 'uid': uid, 'message': message, 'message_type': message_type})

@user_passes_test(allusers)
def teachers(request):
    employees = Users.objects.all()
    return render(request, 'employees/staff.html' ,{'employees':employees})

def generate_password():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    

def delete_files(request):
    pass

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

    return render(request, 'employees/addstaff.html')

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

@require_http_methods(["DELETE"])
def delete_files(request):
    if request.method == 'DELETE':
        try:
            import json
            data = json.loads(request.body)
            item_ids = data.get('ids', [])

            for item_id in item_ids:
                file = Files.objects.get(id=item_id)
                # Delete the file from media storage
                if file.file:
                    default_storage.delete(file.file.path)
                # Delete the file/folder from the database
                file.delete()

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)