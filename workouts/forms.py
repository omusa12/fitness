from django import forms
from django.core.exceptions import ValidationError
from .models import TrainerWorkout, TrainerWorkoutExercise

class TrainerWorkoutForm(forms.ModelForm):
    class Meta:
        model = TrainerWorkout
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TrainerWorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = TrainerWorkoutExercise
        fields = ['trainer_exercise', 'sets', 'reps', 'rest_time', 'notes', 'order']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

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
            existing = TrainerWorkoutExercise.objects.filter(
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

class TrainerWorkoutExerciseFormSet(forms.BaseModelFormSet):
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
