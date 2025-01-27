from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import user_passes_test,login_required
from app.views import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'employees/base.html')

@user_passes_test(allusers)
def dashboard(request):
    return render(request, 'employees/dashboard.html')

@user_passes_test(allusers)
def admincloud(request,uid):
    user = request.user
    files = Files.objects.filter(parent=uid, fk=user.id)
    path = 'root/'

    return render(request, 'employees/cloud.html', {'context': files, 'uid': uid})

@user_passes_test(allusers)
def teachers(request):
    employees = Users.objects.all()
    return render(request, 'employees/teachers.html' ,{'employees':employees})


@user_passes_test(allusers)
@csrf_exempt
def ajax_file_upload(request, dir_id=None):
    if request.method == 'POST' and request.FILES.get('file'):
        file_obj = request.FILES['file']
        file_name = file_obj.name
        file_type = file_obj.content_type.split('/')[1]

        # Use 'dir_id' from the URL as the parent directory
        parent_dir = str(dir_id) if dir_id is not None else ''  # Default to an empty string if no dir provided

        # Check if a file with the same name and type exists in the parent directory
        if Files.objects.filter(name=file_name, ftype=file_type, parent=parent_dir).exists():
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


