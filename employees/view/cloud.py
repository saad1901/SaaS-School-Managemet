from django.shortcuts import render
from employees.models import Files
# from employees.forms import 
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import allusers

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
                # return render(request, 'employees/cloud/cloudtest.html', 
                #             {'context': files, 'uid': uid, 'message': message, 'message_type': message_type})

    storage = round(user.storage / (1024 * 1024), 2)
    max_storage = int(user.max_storage/(1000*1000))
    return render(request, 'employees/cloud/cloudtest.html', 
                {
                'context': files,
                'uid': uid,
                'message': message,
                'message_type': message_type,
                'storage': storage,
                'max_storage': max_storage
                   })
