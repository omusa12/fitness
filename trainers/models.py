from django.db import models
from django.utils.crypto import get_random_string
from users.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

class TrainerProfile(models.Model):
    trainer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    years_of_experience = models.IntegerField(default=0)
    certification = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    available_times = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.trainer.username} Trainer Profile'

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    trainer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='clients')
    fitness_goal = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Client Profile'

class ClientRegistrationToken(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=64, unique=True)
    trainer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(64)
        super().save(*args, **kwargs)

    def send_registration_email(self, request=None):
        if request:
            registration_url = request.build_absolute_uri(
                reverse('client-register') + f'?token={self.token}'
            )
        else:
            registration_url = f"{settings.SITE_URL}{reverse('client-register')}?token={self.token}"
            
        subject = 'Complete Your Fitness Application Registration'
        message = f'''
        Hello {self.first_name},

        Your trainer has created an account for you on the Fitness Application.
        Please click the following link to complete your registration:

        {registration_url}

        If you did not request this registration, please ignore this email.
        '''
        
        print("\n=== Registration Email ===")
        print(f"To: {self.email}")
        print(f"Subject: {subject}")
        print("Message:")
        print(message)
        print("========================\n")
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )
