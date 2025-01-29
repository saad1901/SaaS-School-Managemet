from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.login_view, name='login_view'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)