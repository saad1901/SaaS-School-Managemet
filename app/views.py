from django.shortcuts import render

# Create your views here.
def allusers(user):
    if user.role == 'Teacher' or user.role == 'Super Admin':
        return True

def superadmin(user):
    if user.role == 'Super Admin':
        return True
