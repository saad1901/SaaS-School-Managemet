from django.urls import path
from . import view

urlpatterns = [
    path('', view.dashboard, name='dashboard'),
    path('students', view.students, name='students'),
    path('classes', view.classes, name='classes'),
    path('subjects', view.home, name='subjects'),
    path('reports', view.reports, name='reports'),
    path('addnotes', view.addnotes, name='addnotes'),
    path('posthw', view.home, name='posthw'),
    path('finance', view.home, name='finance'),
    path('settings', view.settings, name='settings'),
    path('settings/permissions', view.settingspermissions, name='settingspermissions'),
    path('settings/storagemanage', view.storagemanage, name='storagemanage'),
    path('profile', view.profile, name='profile'),
    path('profile/edit', view.profile_edit, name='profile_edit'),
    path('profile/edit/<int:id>', view.profile_edit_admin, name='profile_edit_admin'),
    path('profile/edit/credentials/<int:id>', view.credentials, name='credentials'),
    path('delete_files', view.delete_files, name='delete_files'),
    path('employees/addteacher', view.addteacher, name='addteacher'),
    path('logout', view.logoutuser, name='logout'),
    path('employees', view.teachers, name='employees'),
    path('teachercloud/<int:uid>', view.admincloud, name='teachercloud'),
    path('upload-file/<int:dir_id>', view.ajax_file_upload, name='ajax_file_upload'),
    path('delete_folder/<int:id>', view.delete_folder, name='delete_folder'),
    path('addrole', view.addrole, name='addrole'),
    path('getitems', view.get_items, name='getitems'),

]
