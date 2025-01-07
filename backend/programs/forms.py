from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Program, ProgramWorkout, WorkoutExercise
from workouts.models import TrainerWorkout, TrainerExercise

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'description', 'client', 'number_of_weeks', 'is_active']

    def __init__(self, trainer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show clients assigned to this trainer
        self.fields['client'].queryset = trainer.clients.all()
        self.fields['client'].empty_label = "Select a client (optional)"
        self.fields['number_of_weeks'].min_value = 1
        self.fields['number_of_weeks'].help_text = "Number of weeks for the program"

class ProgramWorkoutForm(forms.ModelForm):
    trainer_exercise = forms.ModelChoiceField(
        queryset=TrainerExercise.objects.none(),
        empty_label="Select an exercise from your library",
        required=True
    )
    sets = forms.IntegerField(min_value=1)
    reps = forms.CharField(max_length=50, help_text="e.g., '8-12' or 'Until failure'")
    rest_time = forms.CharField(max_length=50, help_text="e.g., '60s' or '2min'")
    
    class Meta:
        model = ProgramWorkout
        fields = ['name', 'description', 'day_of_week', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, trainer, program=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trainer = trainer
        self.program = program
        # Only show exercises from trainer's library
        self.fields['trainer_exercise'].queryset = TrainerExercise.objects.filter(trainer=trainer)

    def clean(self):
        cleaned_data = super().clean()
        day_of_week = cleaned_data.get('day_of_week')
        order = cleaned_data.get('order')

        if self.program and day_of_week is not None and order is not None:
            # Check if there's already a workout with the same day and order
            existing = ProgramWorkout.objects.filter(
                program=self.program,
                day_of_week=day_of_week,
                order=order
            )
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError(
                    f"A workout with order {order} already exists for this day"
                )
        
        return cleaned_data

    def save(self, commit=True):
        workout = super().save(commit=False)
        if self.program:
            workout.program = self.program
        
        if commit:
            with transaction.atomic():
                workout.save()
                # Create the exercise for this workout
                WorkoutExercise.objects.create(
                    workout=workout,
                    trainer_exercise=self.cleaned_data['trainer_exercise'],
                    sets=self.cleaned_data['sets'],
                    reps=self.cleaned_data['reps'],
                    rest_time=self.cleaned_data['rest_time'],
                    order=0  # First exercise
                )
        
        return workout

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['trainer_exercise', 'sets', 'reps', 'rest_time', 'notes', 'order']

    def __init__(self, trainer, workout=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workout = workout
        # Only show exercises from trainer's library
        self.fields['trainer_exercise'].queryset = trainer.trainerexercise_set.all()

    def clean(self):
        cleaned_data = super().clean()
        order = cleaned_data.get('order')

        if self.workout and order is not None:
            # Check if there's already an exercise with the same order
            existing = WorkoutExercise.objects.filter(
                workout=self.workout,
                order=order
            )
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError(
                    f"An exercise with order {order} already exists in this workout"
                )
        
        return cleaned_data

class WorkoutExerciseFormSet(forms.BaseModelFormSet):
    def clean(self):
        """
        Checks that no two exercises have the same order number.
        """
        if any(self.errors):
            return

        orders = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            order = form.cleaned_data.get('order')
            if order in orders:
                raise ValidationError("Each exercise must have a unique order number.")
            orders.append(order)
