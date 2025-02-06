from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='admin-home'),
    path('', views.dashboard, name='dashboard'),
    path('', views.home, name='students'),
    path('', views.home, name='classes'),
    path('', views.home, name='subjects'),
    path('', views.home, name='reports'),
    path('', views.home, name='postnotes'),
    path('', views.home, name='posthw'),
    path('', views.home, name='finance'),
    path('', views.home, name='settings'),
    path('profile', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/edit/<int:id>', views.profile_edit_admin, name='profile_edit_admin'),
    path('profile/edit/credentials', views.credentials, name='credentials'),
    path('delete_files', views.delete_files, name='delete_files'),
    path('addteacher', views.addteacher, name='addteacher'),
    path('logout', views.logoutuser, name='logout'),
    path('employees', views.teachers, name='employees'),
    path('teachercloud/<int:uid>', views.admincloud, name='teachercloud'),
    path('upload-file/<int:dir_id>', views.ajax_file_upload, name='ajax_file_upload'),
    path('delete-files/', views.delete_files, name='delete_files'),

]
