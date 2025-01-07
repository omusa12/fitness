from django import forms
from django.contrib.auth import get_user_model
from .models import Message, Forum, ForumMessage

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text_content', 'image', 'video']
        widgets = {
            'text_content': forms.Textarea(attrs={'rows': 3}),
        }

class ForumForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Forum
        fields = ['name', 'description', 'participants']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.trainer = kwargs.pop('trainer', None)
        super().__init__(*args, **kwargs)
        if self.trainer:
            # Only show clients of this trainer
            self.fields['participants'].queryset = get_user_model().objects.filter(
                client__trainer=self.trainer
            )

    def clean(self):
        cleaned_data = super().clean()
        if not self.trainer:
            raise ValidationError("Trainer is required to create a forum")
        if not self.trainer.is_trainer:
            raise ValidationError("Only trainers can create forums")
        return cleaned_data

    def save(self, commit=True):
        forum = super().save(commit=False)
        forum.trainer = self.trainer
        if commit:
            forum.save()
            self.save_m2m()  # Save participants
        return forum

class ForumMessageForm(forms.ModelForm):
    class Meta:
        model = ForumMessage
        fields = ['text_content', 'image', 'video']
        widgets = {
            'text_content': forms.Textarea(attrs={'rows': 3}),
        }

class ForumParticipantForm(forms.Form):
    participants = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.trainer = kwargs.pop('trainer', None)
        self.forum = kwargs.pop('forum', None)
        super().__init__(*args, **kwargs)
        if self.trainer:
            # Only show clients of this trainer that aren't already in the forum
            current_participants = self.forum.participants.all() if self.forum else []
            self.fields['participants'].queryset = get_user_model().objects.filter(
                client__trainer=self.trainer
            ).exclude(id__in=[p.id for p in current_participants])
