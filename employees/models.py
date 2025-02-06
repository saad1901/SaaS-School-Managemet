from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model

# Custom User Manager
class EmployeeManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)


# Custom User Model
class Users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(max_length=1, choices=gender_choices)

    date_of_joining = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50, default='Teacher')
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)

    # Address Information
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    hint = models.CharField(max_length=50, blank=True, null=True)
    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # class_under = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    objects = EmployeeManager()

    USERNAME_FIELD = 'email'  # This defines the unique identifier for authentication
    REQUIRED_FIELDS = ['name']  # Fields required when creating a superuser

    def __str__(self):
        return self.name

User = get_user_model()

class Files(models.Model):
    name = models.CharField(max_length=60)
    ftype = models.CharField(max_length=25)
    parent = models.CharField(max_length=60, blank=True, null=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)  # Store files in 'uploads/' directory
    fk = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=20)
    section = models.CharField(max_length=15, blank=True, null=True)
    monitor = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)

# class Student(models.Model):
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),
#     ]
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     date_of_birth = models.DateField()
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15, unique=True)
#     address = models.TextField()
#     admission_date = models.DateField(auto_now_add=True)
#     class_name = models.CharField(max_length=20)
#     roll_number = models.CharField(max_length=20, unique=True)
#     guardian_name = models.CharField(max_length=100)
#     guardian_contact = models.CharField(max_length=15)
#     profile_picture = models.ImageField(upload_to='students/', blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="students")
    
#     def __str__(self):
#         return f"{self.first_name} {self.last_name} ({self.roll_number})"

