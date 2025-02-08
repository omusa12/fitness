from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser, Profile
from django.db import transaction

@receiver(post_save, sender=CustomUser)
def handle_user_profile(sender, instance, created, **kwargs):
    """Handle profile creation and updates for users."""
    with transaction.atomic():
        if created:
            Profile.objects.create(user=instance)
        else:
            # Get or create the profile to handle cases where profile might be missing
            Profile.objects.get_or_create(user=instance)
            # Save any profile updates
            instance.profile.save()
