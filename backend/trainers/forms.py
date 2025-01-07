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

class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ['specialization', 'years_of_experience', 'certification', 'hourly_rate', 'available_times']

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['fitness_goal', 'medical_conditions', 'height', 'weight']
