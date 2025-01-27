from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home', views.home, name='admin-home'),
    path('', views.dashboard, name='dashboard'),
    path('', views.home, name='students'),
    path('teachercloud/<int:uid>', views.admincloud, name='teachercloud'),
    path('', views.home, name='classes'),
    path('', views.home, name='subjects'),
    path('', views.home, name='reports'),
    path('', views.home, name='postnotes'),
    path('', views.home, name='posthw'),
    path('', views.home, name='finance'),
    path('', views.home, name='settings'),
    path('', views.home, name='profile'),
    path('', views.home, name='logout'),
    path('teachers', views.teachers, name='teachers'),
    path('upload-file/<int:dir_id>', views.ajax_file_upload, name='ajax_file_upload'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
