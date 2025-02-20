from django import forms
from .models import Users, SchoolInfo

MAX_STORAGE_CHOICES = [
    (5000000, "5 GB"),
    (10000000, "10 GB"),
    (50000000, "50 GB"),
    (100000000, "100 GB"),  #  Ensure the first value is an integer
    (0, "None"),  #  Ensure the first value is an integer
]


class UserProfileForm(forms.ModelForm):
    max_storage = forms.ChoiceField(choices=MAX_STORAGE_CHOICES, widget=forms.Select)
    class Meta:
        model = Users
        fields = ['name', 'email', 'phone', 'dob', 'gender', 'role', 'max_storage',
                  'address', 'city', 'state', 'postal_code', 'date_of_joining']  # Added `date_of_joining`
        
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'max_storage': forms.NumberInput(attrs={'type': 'number'}),  # Corrected
        }

class SchoolInfoForm(forms.ModelForm):
    class Meta:
        model = SchoolInfo
        fields = "__all__"
