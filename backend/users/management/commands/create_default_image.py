import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates the default profile image in the media directory'

    def handle(self, *args, **kwargs):
        # Create media and default directories if they don't exist
        media_root = settings.MEDIA_ROOT
        default_dir = os.path.join(media_root, 'default')
        os.makedirs(default_dir, exist_ok=True)

        # Path to default image in static files
        static_default = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'default.jpg')
        media_default = os.path.join(default_dir, 'default.jpg')

        try:
            # Copy default image from static to media
            if os.path.exists(static_default):
                shutil.copy2(static_default, media_default)
                self.stdout.write(
                    self.style.SUCCESS('Successfully created default profile image')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Default image not found at {static_default}. '
                        'Please ensure it exists in your static files.'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating default profile image: {str(e)}')
            )
