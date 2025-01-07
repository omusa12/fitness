from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    ]
    
    is_trainer = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='client'
    )
    
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.user_type == 'trainer':
            self.is_trainer = True
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='profile_pics',
        null=True,
        blank=True,
        help_text="Profile picture"
    )
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def image_url(self):
        """Return the URL of the profile image or a placeholder if none exists."""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        # Return a placeholder image URL
        return "https://ui-avatars.com/api/?name=" + self.user.username
