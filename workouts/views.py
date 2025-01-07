from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import HttpResponseForbidden
from django.forms import modelformset_factory
from .models import Exercise, TrainerExercise, TrainerWorkout, TrainerWorkoutExercise
from .forms import TrainerWorkoutForm, TrainerWorkoutExerciseForm, TrainerWorkoutExerciseFormSet

@login_required
def all_exercises(request):
    """View for browsing all exercises from the API."""
    exercises = Exercise.objects.all()
    
    # Get filter parameters
    body_part = request.GET.get('body_part')
    equipment = request.GET.get('equipment')
    target = request.GET.get('target')
    
    # Apply filters if provided
    if body_part:
        exercises = exercises.filter(body_part=body_part)
    if equipment:
        exercises = exercises.filter(equipment=equipment)
    if target:
        exercises = exercises.filter(target=target)
    
    # Get unique values for filter dropdowns
    body_parts = Exercise.objects.values_list('body_part', flat=True).distinct()
    equipment_list = Exercise.objects.values_list('equipment', flat=True).distinct()
    targets = Exercise.objects.values_list('target', flat=True).distinct()
    
    # Get trainer's library for checking if exercise is already added
    library_exercises = TrainerExercise.objects.filter(trainer=request.user)
    
    # Pagination
    paginator = Paginator(exercises, 12)  # Show 12 exercises per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'exercises': page_obj,
        'body_parts': body_parts,
        'equipment_list': equipment_list,
        'targets': targets,
        'library_exercises': library_exercises,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    
    return render(request, 'workouts/all_exercises.html', context)

@login_required
def exercise_library(request):
    """View for browsing and filtering exercises in trainer's library."""
    # Get trainer's library exercises
    trainer_exercises = TrainerExercise.objects.filter(trainer=request.user)
    exercises = Exercise.objects.filter(trainerexercise__trainer=request.user)
    
    # Get filter parameters
    body_part = request.GET.get('body_part')
    equipment = request.GET.get('equipment')
    target = request.GET.get('target')
    
    # Apply filters if provided
    if body_part:
        exercises = exercises.filter(body_part=body_part)
    if equipment:
        exercises = exercises.filter(equipment=equipment)
    if target:
        exercises = exercises.filter(target=target)
    
    # Get unique values for filter dropdowns from trainer's exercises only
    body_parts = exercises.values_list('body_part', flat=True).distinct()
    equipment_list = exercises.values_list('equipment', flat=True).distinct()
    targets = exercises.values_list('target', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(exercises, 12)  # Show 12 exercises per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'exercises': page_obj,
        'body_parts': body_parts,
        'equipment_list': equipment_list,
        'targets': targets,
        'library_exercises': trainer_exercises,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    
    return render(request, 'workouts/exercise_library.html', context)

@login_required
def add_to_library(request, exercise_id):
    """Add an exercise to trainer's library with optional custom video or YouTube link."""
    exercise = get_object_or_404(Exercise, id=exercise_id)
    
    if request.method == 'POST':
        try:
            # Create or update trainer exercise
            trainer_exercise, created = TrainerExercise.objects.get_or_create(
                trainer=request.user,
                exercise=exercise
            )
            
            # Handle custom video upload
            custom_video = request.FILES.get('custom_video')
            if custom_video:
                trainer_exercise.custom_video = custom_video
                trainer_exercise.youtube_link = None  # Clear YouTube link if custom video provided
            
            # Handle YouTube link
            youtube_link = request.POST.get('youtube_link')
            if youtube_link:
                trainer_exercise.youtube_link = youtube_link
                trainer_exercise.custom_video = None  # Clear custom video if YouTube link provided
            
            # Handle notes
            notes = request.POST.get('notes')
            if notes:
                trainer_exercise.notes = notes
            
            # Save the changes
            trainer_exercise.save()
            
            messages.success(request, f'{exercise.name} has been added to your library.')
            
        except ValidationError as e:
            messages.error(request, str(e))
        except IntegrityError:
            messages.error(request, 'This exercise is already in your library.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('workouts:exercise_library')

@login_required
def workout_template_list(request):
    """View for listing all workout templates created by the trainer."""
    if not request.user.is_trainer:
        return HttpResponseForbidden("Only trainers can access workout templates.")
    
    workouts = TrainerWorkout.objects.filter(trainer=request.user)
    return render(request, 'workouts/workout_template_list.html', {'workouts': workouts})

@login_required
def workout_template_create(request):
    """View for creating a new workout template."""
    if not request.user.is_trainer:
        return HttpResponseForbidden("Only trainers can create workout templates.")
    
    if request.method == 'POST':
        form = TrainerWorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.trainer = request.user
            workout.save()
            messages.success(request, 'Workout template created successfully.')
            return redirect('workouts:workout_template_exercises', workout_pk=workout.pk)
    else:
        form = TrainerWorkoutForm()
    
    return render(request, 'workouts/workout_template_form.html', {
        'form': form,
        'title': 'Create Workout Template'
    })

@login_required
def workout_template_edit(request, pk):
    """View for editing a workout template."""
    workout = get_object_or_404(TrainerWorkout, pk=pk)
    
    if request.user != workout.trainer:
        return HttpResponseForbidden("You don't have permission to edit this workout template.")
    
    if request.method == 'POST':
        form = TrainerWorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workout template updated successfully.')
            return redirect('workouts:workout_template_list')
    else:
        form = TrainerWorkoutForm(instance=workout)
    
    return render(request, 'workouts/workout_template_form.html', {
        'form': form,
        'title': 'Edit Workout Template'
    })

@login_required
def workout_template_delete(request, pk):
    """View for deleting a workout template."""
    workout = get_object_or_404(TrainerWorkout, pk=pk)
    
    if request.user != workout.trainer:
        return HttpResponseForbidden("You don't have permission to delete this workout template.")
    
    if request.method == 'POST':
        workout.delete()
        messages.success(request, 'Workout template deleted successfully.')
        return redirect('workouts:workout_template_list')
    
    return render(request, 'workouts/workout_template_confirm_delete.html', {'workout': workout})

@login_required
def workout_template_exercises(request, workout_pk):
    """View for managing exercises in a workout template."""
    workout = get_object_or_404(TrainerWorkout, pk=workout_pk)
    
    if request.user != workout.trainer:
        return HttpResponseForbidden("You don't have permission to manage exercises in this workout template.")
    
    ExerciseFormSet = modelformset_factory(
        TrainerWorkoutExercise,
        form=TrainerWorkoutExerciseForm,
        formset=TrainerWorkoutExerciseFormSet,
        extra=1,
        can_delete=True
    )
    
    if request.method == 'POST':
        formset = ExerciseFormSet(
            request.POST,
            queryset=TrainerWorkoutExercise.objects.filter(workout=workout),
            form_kwargs={'trainer': request.user, 'workout': workout}
        )
        if formset.is_valid():
            instances = formset.save(commit=False)
            
            with transaction.atomic():
                # Delete marked objects
                for obj in formset.deleted_objects:
                    obj.delete()
                
                # Save new/updated objects
                for instance in instances:
                    instance.workout = workout
                    instance.save()
            
            messages.success(request, 'Exercises updated successfully.')
            return redirect('workouts:workout_template_list')
    else:
        formset = ExerciseFormSet(
            queryset=TrainerWorkoutExercise.objects.filter(workout=workout),
            form_kwargs={'trainer': request.user, 'workout': workout}
        )
    
    return render(request, 'workouts/workout_template_exercises.html', {
        'formset': formset,
        'workout': workout
    })
