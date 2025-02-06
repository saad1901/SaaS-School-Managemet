from django import forms
from .models import Users

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'email', 'phone', 'dob', 'gender', 
                  'address', 'city', 'state', 'postal_code']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }
