from django.urls import path
from . import views
from . import view

urlpatterns = [
    path('', view.dashboard, name='dashboard'),
    path('students', view.students, name='students'),
    path('classes', views.home, name='classes'),
    path('subjects', views.home, name='subjects'),
    path('reports', views.reports, name='reports'),
    path('postnotes', views.home, name='postnotes'),
    path('posthw', views.home, name='posthw'),
    path('finance', views.home, name='finance'),
    path('settings', views.settings, name='settings'),
    path('profile', view.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/edit/<int:id>', views.profile_edit_admin, name='profile_edit_admin'),
    path('profile/edit/credentials/<int:id>', views.credentials, name='credentials'),
    path('delete_files', views.delete_files, name='delete_files'),
    path('employees/addteacher', view.addteacher, name='addteacher'),
    path('logout', views.logoutuser, name='logout'),
    path('employees', view.teachers, name='employees'),
    path('teachercloud/<int:uid>', views.admincloud, name='teachercloud'),
    path('upload-file/<int:dir_id>', view.ajax_file_upload, name='ajax_file_upload'),
    path('delete-files/', view.delete_files, name='delete_files'),
    path('delete_folder/<int:id>', view.delete_folder, name='delete_folder'),
    path('addrole', views.addrole, name='addrole')

]
