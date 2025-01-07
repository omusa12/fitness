from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

class Message(models.Model):
    conversation = models.ForeignKey(
        'Conversation',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    text_content = models.TextField(blank=True)
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)
    video = models.FileField(upload_to='message_videos/', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        constraints = [
            models.UniqueConstraint(
                fields=['sender', 'recipient', 'conversation', 'text_content', 'timestamp'],
                name='unique_message_within_timeframe'
            )
        ]

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient} at {self.timestamp}'

class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    last_message = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-last_message']

    def clean(self):
        super().clean()
        if self.pk and self.participants.count() != 2:
            raise ValidationError('Conversation must have exactly two participants.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_other_participant(self, user):
        """Get the other participant in the conversation."""
        return self.participants.exclude(id=user.id).first()

    def __str__(self):
        return f'Conversation between {", ".join(str(p) for p in self.participants.all())}'

class Forum(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='moderated_forums'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='forum_memberships'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-last_activity']

    def clean(self):
        super().clean()
        # Ensure trainer is actually a trainer
        if hasattr(self, 'trainer') and self.trainer is not None:
            if not self.trainer.is_trainer:
                raise ValidationError('Forum moderator must be a trainer.')

    def save(self, *args, **kwargs):
        self.clean()
        is_new = self.pk is None  # Check if this is a new forum
        super().save(*args, **kwargs)
        if is_new:  # Only add trainer as participant on creation
            self.participants.add(self.trainer)

    def __str__(self):
        return self.name

class ForumMessage(models.Model):
    forum = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='forum_messages'
    )
    text_content = models.TextField(blank=True)
    image = models.ImageField(upload_to='forum_images/', blank=True, null=True)
    video = models.FileField(upload_to='forum_videos/', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def clean(self):
        super().clean()
        # Ensure sender is a forum participant
        if hasattr(self, 'forum') and self.forum is not None and hasattr(self, 'sender') and self.sender is not None:
            # Allow both trainer and participants to post messages
            if self.sender != self.forum.trainer and not self.forum.participants.filter(id=self.sender.id).exists():
                raise ValidationError('Message sender must be the trainer or a forum participant.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        # Update forum's last activity
        self.forum.last_activity = timezone.now()
        self.forum.save(update_fields=['last_activity'])

    def __str__(self):
        return f'Forum message from {self.sender} in {self.forum} at {self.timestamp}'
