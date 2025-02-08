from django import forms
from django.forms import BaseModelFormSet
from .models import Program, ProgramWorkout, WorkoutExercise
from workouts.models import TrainerExercise

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'description', 'client', 'number_of_weeks', 'start_date', 'is_active']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = user.clients.all()

class ProgramWorkoutForm(forms.ModelForm):
    trainer_exercise = forms.ModelChoiceField(queryset=None)
    sets = forms.IntegerField(min_value=1)
    reps = forms.CharField(max_length=50, help_text="e.g., '8-12' or 'Until failure'")
    rest_time = forms.CharField(max_length=50, help_text="e.g., '60s' or '2min'")

    class Meta:
        model = ProgramWorkout
        fields = ['day_of_week', 'order']

    def __init__(self, user, program, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trainer_exercise'].queryset = TrainerExercise.objects.filter(trainer=user)
        self.program = program

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.program = self.program
        if commit:
            instance.save()
        return instance

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['trainer_exercise', 'sets', 'reps', 'rest_time', 'notes', 'order']

    def __init__(self, trainer=None, workout=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if trainer:
            self.fields['trainer_exercise'].queryset = TrainerExercise.objects.filter(trainer=trainer)
        self.workout = workout

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.workout:
            instance.workout = self.workout
        if commit:
            instance.save()
        return instance

class WorkoutExerciseFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        orders = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                order = form.cleaned_data.get('order')
                if order in orders:
                    raise forms.ValidationError('Each exercise must have a unique order.')
                orders.append(order)

class WorkoutSectionForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, required=False)
    section_type = forms.ChoiceField(choices=ProgramWorkout.SECTION_TYPES)
    days = forms.MultipleChoiceField(
        choices=[
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        ],
        widget=forms.CheckboxSelectMultiple
    )
