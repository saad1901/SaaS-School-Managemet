from . import views
from django.urls import path

urlpatterns = [
    path('', views.login_view, name='login_view'),

]