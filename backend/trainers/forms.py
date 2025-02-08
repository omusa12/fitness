from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from .models import TrainerProfile, Client

class TrainerRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'trainer'
        if commit:
            user.save()
        return user

class ClientPreRegistrationForm(forms.Form):
    email = forms.EmailField(label='Client Email')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

class ClientRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'client'
        if commit:
            user.save()
        return user

class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ['specialization', 'years_of_experience', 'certification', 'hourly_rate', 'available_times']

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['fitness_goal', 'medical_conditions', 'height', 'height_unit', 'height_inches', 'weight', 'weight_unit']
        widgets = {
            'fitness_goal': forms.Select(attrs={'class': 'form-control'}),
            'medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'height_unit': forms.Select(attrs={'class': 'form-control'}),
            'height_inches': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'weight_unit': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'height': 'Enter height in feet (if using ft/in) or centimeters',
            'height_inches': 'If using feet/inches, enter the inches portion here',
            'weight': 'Enter weight in your chosen unit (kg or lb)',
        }
