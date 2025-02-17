from django.shortcuts import render
from employees.models import Class, Users, Roles
from django.contrib.auth.decorators import user_passes_test, login_required
from app.views import allusers, superadmin

@login_required
@user_passes_test(allusers)
def teachers(request):
    if request.user.role == 'Super Admin':
        employees = Users.objects.all()
    else:
        employees = Users.objects.exclude(role = 'Super Admin')
    classes = Class.objects.all()
    return render(request, 'employees/staff/staff.html' ,{'employees':employees})

def generate_password():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
 
@login_required
@user_passes_test(superadmin)
def addteacher(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        date_of_joining = request.POST.get("date_of_joining")
        role = request.POST.get("role")
        salary = request.POST.get("salary") or None
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal_code = request.POST.get("postal_code")
        password = generate_password()
        print(password)
        hashed_password = make_password(password)
        Users.objects.create(
            name=name, email=email, phone=phone, dob=dob, gender=gender,
            date_of_joining=date_of_joining, role=role, salary=salary,
            address=address, city=city, state=state, postal_code=postal_code, password=hashed_password, hint=password
        )

        return redirect("employees")
    roles = Roles.objects.exclude(name = 'Super Admin')
    return render(request, 'employees/staff/addstaff.html',{'roles':roles})
# 