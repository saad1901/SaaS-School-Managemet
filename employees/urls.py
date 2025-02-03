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
    path('', views.home, name='profile'),
    path('addteacher', views.addteacher, name='addteacher'),
    path('logout', views.logoutuser, name='logout'),
    path('teachers', views.teachers, name='teachers'),
    path('teachercloud/<int:uid>', views.admincloud, name='teachercloud'),
    path('upload-file/<int:dir_id>', views.ajax_file_upload, name='ajax_file_upload'),

]
