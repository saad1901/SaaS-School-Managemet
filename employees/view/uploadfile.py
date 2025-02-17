from django.shortcuts import render, redirect
from employees.models import Users, Files, Class
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import allusers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
import math

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
def addnotes(request):
    classes = []
    if request.user.role == 'Teacher' or request.user.role =='Super Admin':
        classes = Class.objects.filter(monitor=request.user)
    return render(request, 'employees/students/addnotes.html',{'classes':classes})



