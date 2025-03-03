from django.shortcuts import render, redirect
from employees.models import Users, Files, Class, Notes
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
        user = request.user 
        uploaded_size = uploaded_file.size / 1024 
        print(int(uploaded_size))
        if user.storage + uploaded_size > user.max_storage:
            # print(user.storage + uploaded_size)
            # print(user.max_storage)
            print('I was called')
            return JsonResponse({'message': 'Storage Limit has been Hit! Contact Admin'}, status=400)
        # Update storage usage
        Users.objects.filter(id=user.id).update(storage=user.storage + int(uploaded_size))

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
                'message': 'This file already exists in this directory.'
            }, status=400)

        # Save the file to the database
        file_instance = Files.objects.create(
            name=file_name,
            ftype=file_type,
            file=file_obj,
            fk=request.user, 
            parent=parent_dir,
            file_size=file_size,
            sizeinkb = int(uploaded_size)
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
        user = request.user
        try:
            import json
            data = json.loads(request.body)
            item_ids = data.get('ids', [])
            totalsizeinkb = 0

            for item_id in item_ids:
                file = Files.objects.get(id=item_id)
                if file.file:
                    totalsizeinkb = totalsizeinkb + file.sizeinkb
                    default_storage.delete(file.file.path)
                # Delete the file/folder from the database
                file.delete()
            
            Users.objects.filter(id=user.id).update(storage=user.storage - totalsizeinkb)

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def deletefunc(id):
    folder = Files.objects.get(id=id)
    totalsizeinkb = 0
    if Files.objects.filter(parent=id).exists():
        
        subfiles = Files.objects.filter(parent=id)
        for file in subfiles:
            if file.ftype == 'folder':
                totalsizeinkb = totalsizeinkb + deletefunc(file.id)
            else:
                totalsizeinkb = totalsizeinkb + file.sizeinkb
                default_storage.delete(file.file.path)
                file.delete()

    folder.delete()
    return totalsizeinkb

@login_required
@user_passes_test(allusers)
def delete_folder(request, id):
    user = request.user
    if Files.objects.get(id=id).ftype == 'folder':
        return_id = Files.objects.get(id=id).parent
        # totalsizeinkb = deletefunc(id)
        Users.objects.filter(id=user.id).update(storage=user.storage - deletefunc(id))
    return redirect('teachercloud', uid=return_id)


### NOTES SECTION ###


@login_required
@user_passes_test(allusers)
def addnotes(request):
    classes = []
    if request.user.role == 'Teacher' or request.user.role =='Super Admin':
        classes = Class.objects.filter(monitor=request.user)

    return render(request, 'employees/students/addnotes.html',{'classes':classes})


@login_required
@user_passes_test(allusers)
def get_items(request):
    # Use the same query parameter names as in your JavaScript
    
    classfor_param = request.GET.get('classfor')
    parent_param = request.GET.get('parent')


    if not parent_param:
        parent_param = 0

    # parent_param = 0
    if parent_param is not 0:
        items = Notes.objects.filter(parent=parent_param)
    else:
        items = Notes.objects.filter(classfor=classfor_param, parent=parent_param)
    
    data = {
        'items': [
            {
                'id': item.id,
                'name': item.name,
                'is_folder': item.ftype == 'Folder',  # Check if ftype is 'folder'
                'type': item.ftype,
            }
            for item in items
        ]
    }
    print(data)
    return JsonResponse(data)

