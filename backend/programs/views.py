from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from django.db import transaction, models
from django.http import HttpResponseForbidden
from .models import Program, ProgramWorkout, WorkoutExercise
from workouts.models import TrainerExercise
from .forms import (
    ProgramForm, ProgramWorkoutForm, WorkoutExerciseForm, 
    WorkoutExerciseFormSet, WorkoutSectionForm
)

@login_required
def program_list(request):
    """View for listing all programs created by the trainer."""
    if not request.user.is_trainer:
        return HttpResponseForbidden("Only trainers can access this page.")
    
    programs = Program.objects.filter(trainer=request.user)
    return render(request, 'programs/program_list.html', {'programs': programs})

@login_required
def program_detail(request, pk):
    """View for showing program details."""
    program = get_object_or_404(Program, pk=pk)
    
    # Only allow trainer who created the program or assigned client to view
    if request.user != program.trainer and request.user != program.client:
        return HttpResponseForbidden("You don't have permission to view this program.")
    
    return render(request, 'programs/program_detail.html', {'program': program})

@login_required
def program_create(request):
    """View for creating a new program."""
    if not request.user.is_trainer:
        return HttpResponseForbidden("Only trainers can create programs.")
    
    if request.method == 'POST':
        form = ProgramForm(request.user, request.POST)
        if form.is_valid():
            program = form.save(commit=False)
            program.trainer = request.user
            program.save()
            messages.success(request, 'Program created successfully.')
            return redirect('programs:program_detail', pk=program.pk)
    else:
        form = ProgramForm(request.user)
    
    return render(request, 'programs/program_form.html', {
        'form': form,
        'title': 'Create Program'
    })

@login_required
def program_edit(request, pk):
    """View for editing an existing program."""
    program = get_object_or_404(Program, pk=pk)
    
    if request.user != program.trainer:
        return HttpResponseForbidden("You don't have permission to edit this program.")
    
    if request.method == 'POST':
        form = ProgramForm(request.user, request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program updated successfully.')
            return redirect('programs:program_detail', pk=program.pk)
    else:
        form = ProgramForm(request.user, instance=program)
    
    return render(request, 'programs/program_form.html', {
        'form': form,
        'title': 'Edit Program'
    })

@login_required
def program_delete(request, pk):
    """View for deleting a program."""
    program = get_object_or_404(Program, pk=pk)
    
    if request.user != program.trainer:
        return HttpResponseForbidden("You don't have permission to delete this program.")
    
    if request.method == 'POST':
        program.delete()
        messages.success(request, 'Program deleted successfully.')
        return redirect('programs:program_list')
    
    return render(request, 'programs/program_confirm_delete.html', {'program': program})

@login_required
def workout_create(request, program_pk):
    """View for adding a workout to a program."""
    program = get_object_or_404(Program, pk=program_pk)
    
    if request.user != program.trainer:
        return HttpResponseForbidden("You don't have permission to add workouts to this program.")
    
    # Check if trainer has any exercises in their library
    if not TrainerExercise.objects.filter(trainer=request.user).exists():
        messages.warning(request, 'You need to add exercises to your library before creating workouts. Please add exercises to your library first.')
        return redirect('workouts:all_exercises')
    
    if request.method == 'POST':
        form = ProgramWorkoutForm(request.user, program, request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            # Set default name based on day and order
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            workout.name = f"{day_names[workout.day_of_week]} Workout {workout.order}"
            workout.save()
            messages.success(request, 'Workout added successfully.')
            return redirect('programs:program_detail', pk=program.pk)
    else:
        form = ProgramWorkoutForm(request.user, program)
    
    return render(request, 'programs/workout_form.html', {
        'form': form,
        'program': program,
        'title': 'Add Workout'
    })

@login_required
def workout_edit(request, pk):
    """View for editing a workout."""
    workout = get_object_or_404(ProgramWorkout, pk=pk)
    
    if request.user != workout.program.trainer:
        return HttpResponseForbidden("You don't have permission to edit this workout.")
    
    # Check if trainer has any exercises in their library
    if not TrainerExercise.objects.filter(trainer=request.user).exists():
        messages.warning(request, 'You need to add exercises to your library before editing workouts. Please add exercises to your library first.')
        return redirect('workouts:all_exercises')
    
    # Get the first exercise for this workout to pre-populate the form
    workout_exercise = workout.exercises.first()
    initial_data = {}
    if workout_exercise:
        initial_data = {
            'trainer_exercise': workout_exercise.trainer_exercise,
            'sets': workout_exercise.sets,
            'reps': workout_exercise.reps,
            'rest_time': workout_exercise.rest_time
        }
    
    if request.method == 'POST':
        form = ProgramWorkoutForm(request.user, workout.program, request.POST, instance=workout)
        if form.is_valid():
            with transaction.atomic():
                # Save the workout with auto-generated name
                workout = form.save(commit=False)
                day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                workout.name = f"{day_names[workout.day_of_week]} Workout {workout.order}"
                workout.save()
                # Update the exercise
                if workout_exercise:
                    workout_exercise.trainer_exercise = form.cleaned_data['trainer_exercise']
                    workout_exercise.sets = form.cleaned_data['sets']
                    workout_exercise.reps = form.cleaned_data['reps']
                    workout_exercise.rest_time = form.cleaned_data['rest_time']
                    workout_exercise.save()
                else:
                    WorkoutExercise.objects.create(
                        workout=workout,
                        trainer_exercise=form.cleaned_data['trainer_exercise'],
                        sets=form.cleaned_data['sets'],
                        reps=form.cleaned_data['reps'],
                        rest_time=form.cleaned_data['rest_time'],
                        order=0
                    )
            messages.success(request, 'Workout updated successfully.')
            return redirect('programs:program_detail', pk=workout.program.pk)
    else:
        form = ProgramWorkoutForm(request.user, workout.program, instance=workout, initial=initial_data)
    
    return render(request, 'programs/workout_form.html', {
        'form': form,
        'program': workout.program,
        'title': 'Edit Workout'
    })

@login_required
def workout_delete(request, pk):
    """View for deleting a workout."""
    workout = get_object_or_404(ProgramWorkout, pk=pk)
    
    if request.user != workout.program.trainer:
        return HttpResponseForbidden("You don't have permission to delete this workout.")
    
    if request.method == 'POST':
        program_pk = workout.program.pk
        workout.delete()
        messages.success(request, 'Workout deleted successfully.')
        return redirect('programs:program_detail', pk=program_pk)
    
    return render(request, 'programs/workout_confirm_delete.html', {'workout': workout})

@login_required
def workout_exercises(request, workout_pk):
    """View for managing exercises in a workout."""
    workout = get_object_or_404(ProgramWorkout, pk=workout_pk)
    
    if request.user != workout.program.trainer:
        return HttpResponseForbidden("You don't have permission to manage exercises in this workout.")
    
    ExerciseFormSet = modelformset_factory(
        WorkoutExercise,
        form=WorkoutExerciseForm,
        formset=WorkoutExerciseFormSet,
        extra=1,
        can_delete=True
    )
    
    if request.method == 'POST':
        formset = ExerciseFormSet(
            request.POST,
            queryset=WorkoutExercise.objects.filter(workout=workout),
            form_kwargs={'trainer': request.user, 'workout': workout}
        )
        if formset.is_valid():
            instances = formset.save(commit=False)
            
            # Handle the formset in a transaction
            with transaction.atomic():
                # Delete marked objects
                for obj in formset.deleted_objects:
                    obj.delete()
                
                # Save new/updated objects
                for instance in instances:
                    instance.workout = workout
                    instance.save()
            
            messages.success(request, 'Exercises updated successfully.')
            return redirect('programs:program_detail', pk=workout.program.pk)
    else:
        formset = ExerciseFormSet(
            queryset=WorkoutExercise.objects.filter(workout=workout),
            form_kwargs={'trainer': request.user, 'workout': workout}
        )
    
    return render(request, 'programs/workout_exercises.html', {
        'formset': formset,
        'workout': workout
    })

@login_required
@login_required
def edit_workout_section(request, program_pk, section_name):
    """View for editing workout sections across multiple days."""
    program = get_object_or_404(Program, pk=program_pk)
    
    if request.user != program.trainer:
        return HttpResponseForbidden("You don't have permission to edit workouts in this program.")
    
    # Get all sections with this name
    sections = ProgramWorkout.objects.filter(program=program, name=section_name)
    if not sections.exists():
        messages.error(request, 'Section not found.')
        return redirect('programs:program_detail', pk=program_pk)
    
    # Get the days where this section exists
    current_days = [str(section.day_of_week) for section in sections]
    
    if request.method == 'POST':
        form = WorkoutSectionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Update existing sections
                sections.update(
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                    section_type=form.cleaned_data['section_type']
                )
                
                # Get the selected days
                new_days = form.cleaned_data['days']
                
                # Remove section from unselected days
                sections.filter(day_of_week__in=[int(d) for d in current_days if d not in new_days]).delete()
                
                # Add section to newly selected days
                for day in new_days:
                    if str(day) not in current_days:
                        # Get the highest order for this day
                        max_order = ProgramWorkout.objects.filter(
                            program=program,
                            day_of_week=day
                        ).aggregate(models.Max('order'))['order__max']
                        
                        # If no workouts exist for this day, start with order 0
                        next_order = (max_order + 1) if max_order is not None else 0
                        
                        # Create the workout section
                        ProgramWorkout.objects.create(
                            program=program,
                            name=form.cleaned_data['name'],
                            description=form.cleaned_data['description'],
                            section_type=form.cleaned_data['section_type'],
                            day_of_week=day,
                            order=next_order
                        )
            
            messages.success(request, 'Workout sections updated successfully.')
            return redirect('programs:program_detail', pk=program.pk)
    else:
        # Get initial data from first section
        first_section = sections.first()
        form = WorkoutSectionForm(initial={
            'name': first_section.name,
            'description': first_section.description,
            'section_type': first_section.section_type,
            'days': current_days
        })
    
    return render(request, 'programs/edit_workout_section.html', {
        'form': form,
        'program': program,
        'section_name': section_name
    })

def add_workout_section(request, program_pk):
    """View for adding workout sections to multiple days."""
    program = get_object_or_404(Program, pk=program_pk)
    
    if request.user != program.trainer:
        return HttpResponseForbidden("You don't have permission to add workouts to this program.")
    
    if request.method == 'POST':
        form = WorkoutSectionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                for day in form.cleaned_data['days']:
                    # Get the highest order for this day
                    max_order = ProgramWorkout.objects.filter(
                        program=program,
                        day_of_week=day
                    ).aggregate(models.Max('order'))['order__max']
                    
                    # If no workouts exist for this day, start with order 0
                    next_order = (max_order + 1) if max_order is not None else 0
                    
                    # Create the workout section
                    ProgramWorkout.objects.create(
                        program=program,
                        name=form.cleaned_data['name'],
                        description=form.cleaned_data['description'],
                        section_type=form.cleaned_data['section_type'],
                        day_of_week=day,
                        order=next_order
                    )
            
            messages.success(request, 'Workout sections added successfully.')
            return redirect('programs:program_detail', pk=program.pk)
    else:
        form = WorkoutSectionForm()
    
    return render(request, 'programs/add_workout_section.html', {
        'form': form,
        'program': program
    })
