from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """Create a Profile for new users."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    """Save the user's profile."""
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Create profile if it doesn't exist
        Profile.objects.create(user=instance)
