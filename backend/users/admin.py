from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'is_trainer', 'is_staff', 'is_active',)
    list_filter = ('user_type', 'is_trainer', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('User Type', {'fields': ('user_type', 'is_trainer')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'user_type', 'password1', 'password2',
                'is_staff', 'is_active'
            )}
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_of_birth')
    list_filter = ('date_of_birth',)
    search_fields = ('user__username', 'phone_number')
    raw_id_fields = ('user',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
