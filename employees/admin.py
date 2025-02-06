from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Files, Class

class EmployeeAdmin(UserAdmin):
    # Display fields in the admin panel
    list_display = ('email', 'name', 'is_staff', 'is_active', 'role')
    list_filter = ('is_staff', 'is_active', 'role')
    search_fields = ('email', 'name')
    ordering = ('email',)

    # Define fieldsets for the admin panel
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'dob', 'phone', 'gender', 'role', 'salary', 'address', 'city', 'state', 'postal_code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(Users, EmployeeAdmin)
admin.site.register(Files)
admin.site.register(Class)
