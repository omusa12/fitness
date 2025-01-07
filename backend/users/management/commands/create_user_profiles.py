from django.core.management.base import BaseCommand
from users.models import CustomUser, Profile
from trainers.models import TrainerProfile, Client

class Command(BaseCommand):
    help = 'Creates missing profiles for existing users'

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.all()
        for user in users:
            # Create user profile if it doesn't exist
            Profile.objects.get_or_create(user=user)
            
            # Create trainer or client profile if it doesn't exist
            if user.user_type == 'trainer':
                TrainerProfile.objects.get_or_create(trainer=user)
            elif user.user_type == 'client':
                Client.objects.get_or_create(user=user)
            
        self.stdout.write(self.style.SUCCESS('Successfully created missing profiles'))
