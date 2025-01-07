from django.core.management.base import BaseCommand
from workouts.services import ExerciseDBService

class Command(BaseCommand):
    help = 'Syncs exercises from ExerciseDB API to the local database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=1000,
            help='Number of exercises to sync (default: 1000)'
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting exercise sync...')
        
        service = ExerciseDBService()
        success = service.sync_exercises(limit=options['limit'])
        
        if success:
            self.stdout.write(self.style.SUCCESS('Successfully synced exercises'))
        else:
            self.stdout.write(self.style.ERROR('Failed to sync exercises'))
