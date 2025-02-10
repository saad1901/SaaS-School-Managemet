from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .forms import UserProfileForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import authenticate, login, logout
import math

@login_required
@user_passes_test(allusers)
def profile(request):
    return render(request, 'employees/profile.html')

@login_required
@user_passes_test(allusers)
def credentials(request, id):
    print('credentials id = ', id)
    user = Users.objects.get(id=id)

    print('credentials name = ', user.name)
    if request.method == 'POST':
        password = request.POST.get('password')

        # Validate password length and complexity (Optional)
        if len(password) < 8 or not any(char.isdigit() for char in password) \
           or not any(char.islower() for char in password) \
           or not any(char.isupper() for char in password):
            messages.error(request, "Password must contain at least 8 characters, one uppercase, one lowercase, and one number.")
            return render(request, 'employees/credentials.html')

        user.password = make_password(password)
        user.hint = password
        user.save()
        if id == request.user.id:
            print('i am called')
            login(request, user)
        messages.success(request, "Your password has been successfully updated!")

    return render(request, 'employees/credentials.html', {'user':user,'id': id})

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
    return render(request, 'employees/profile_edit.html', {'form': form,'id':user.id, 'personal': True})

@login_required
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

@login_required
@user_passes_test(allusers)
def dashboard(request):
    classes = []
    if request.user.role == 'Teacher':
        # return render(request, 'employees/superadmin_dashboard.html')
        classes = Class.objects.filter(monitor=request.user)
    total_employees = Users.objects.filter(role='Teacher').count()
    return render(request, 'employees/dashboard.html', {'classes': classes, 'total_employees': total_employees})

@login_required
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

@login_required
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

@login_required
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

@login_required
@user_passes_test(allusers)
@csrf_exempt
def ajax_file_upload(request, dir_id=None):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file: InMemoryUploadedFile = request.FILES['file']
        max_size = 100 * 1024 * 1024

        if uploaded_file.size > max_size:
            return JsonResponse({'message': 'File size must be less than 100MB.'}, status=400)

        file_obj = request.FILES['file']
        file_name = file_obj.name

        # Convert size to KB or MB, rounding up
        if file_obj.size > 1024 * 1024:
            file_size = str(math.ceil(file_obj.size / (1024 * 1024))) + ' MB'
        else:
            file_size = str(math.ceil(file_obj.size / 1024)) + ' KB'

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
            parent=parent_dir,
            file_size=file_size
        )

        return JsonResponse({
            'message': 'File uploaded successfully',
            'file_url': file_instance.file.url
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
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


def deletefunc(id):
    folder = Files.objects.get(id=id)
    if Files.objects.filter(parent=id).exists():
        subfiles = Files.objects.filter(parent=id)
        for file in subfiles:
            if file.ftype == 'folder':
                deletefunc(file.id)
            else:
                default_storage.delete(file.file.path)
                file.delete()

    folder.delete()


@login_required
@user_passes_test(allusers)
def delete_folder(request, id):
    if Files.objects.get(id=id).ftype == 'folder':
        return_id = Files.objects.get(id=id).parent
        deletefunc(id)
    return redirect('teachercloud', uid=return_id)

@login_required
@user_passes_test(allusers)
def reports(request):
    return render(request, 'employees/reports.html')