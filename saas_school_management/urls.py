from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from app.views import login_view
urlpatterns = [
    path('superadmin', admin.site.urls, name='superadmin'),
    # path('', include('app.urls')),
    path('', login_view, name='login_view'),
    path('admin/', include('employees.urls'), name='admin'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
