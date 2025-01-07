from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_type = forms.ChoiceField(
        choices=[choice for choice in CustomUser.USER_TYPE_CHOICES if choice[0] != 'admin']
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'date_of_birth', 'phone_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'client'
        if commit:
            user.save()
        return user
