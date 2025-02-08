from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
import json
from datetime import datetime
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from .forms import (
    TrainerRegistrationForm, ClientPreRegistrationForm, 
    ClientRegistrationForm, ClientProfileForm
)
from .models import ClientRegistrationToken, TrainerProfile, Client
from django.contrib.auth import login
from users.models import CustomUser
from programs.models import Program

@login_required
def trainer_home(request):
    if request.user.user_type != 'trainer':
        messages.error(request, 'Only trainers can access this page')
        return redirect('dashboard')
    
    clients = Client.objects.filter(trainer=request.user).select_related('user', 'user__profile')
    return render(request, 'trainers/trainer_home.html', {'clients': clients})


@login_required
def client_detail(request, client_id):
    if request.user.user_type != 'trainer':
        return HttpResponseForbidden('Only trainers can access this page')
    
    client = get_object_or_404(Client, id=client_id, trainer=request.user)
    return render(request, 'trainers/client_detail.html', {'client': client})

@login_required
def client_calendar(request, client_id):
    if request.user.user_type != 'trainer':
        return HttpResponseForbidden('Only trainers can access this page')
    
    client = get_object_or_404(Client, id=client_id, trainer=request.user)
    
    # Get programs assigned to this client
    assigned_programs = Program.objects.filter(
        client=client.user,
        is_active=True,
        start_date__isnull=False
    )
    
    # Format programs for FullCalendar
    calendar_events = []
    from datetime import timedelta
    for program in assigned_programs:
        end_date = program.start_date + timedelta(weeks=program.number_of_weeks)
        calendar_events.append({
            'title': program.name,
            'start': program.start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'),
            'url': reverse('programs:program_detail', args=[program.id]),
            'backgroundColor': '#007bff',
            'borderColor': '#0056b3'
        })
    
    # Get available programs (unassigned or templates)
    available_programs = Program.objects.filter(
        trainer=request.user,
        client__isnull=True,
        is_active=True
    )
    
    # Serialize the calendar events to JSON
    calendar_events_json = json.dumps(calendar_events)
    
    context = {
        'client': client,
        'assigned_programs': calendar_events_json,
        'available_programs': available_programs,
    }
    
    return render(request, 'trainers/client_calendar.html', context)

@login_required
@require_POST
def assign_program(request, client_id):
    if request.user.user_type != 'trainer':
        return HttpResponseForbidden('Only trainers can access this page')
    
    client = get_object_or_404(Client, id=client_id, trainer=request.user)
    
    try:
        program_id = request.POST.get('program')
        start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
        
        # Get the program template
        program_template = get_object_or_404(Program, id=program_id, trainer=request.user)
        
        # Create a new program instance for the client
        new_program = Program.objects.create(
            name=program_template.name,
            description=program_template.description,
            trainer=request.user,
            client=client.user,
            number_of_weeks=program_template.number_of_weeks,
            start_date=start_date
        )
        
        # Copy workouts from template
        for workout in program_template.workouts.all():
            new_workout = workout
            new_workout.pk = None
            new_workout.program = new_program
            new_workout.save()
            
            # Copy exercises
            for exercise in workout.exercises.all():
                new_exercise = exercise
                new_exercise.pk = None
                new_exercise.workout = new_workout
                new_exercise.save()
        
        messages.success(request, f'Program "{new_program.name}" has been assigned to {client.user.get_full_name()}')
        return redirect('trainers:client_calendar', client_id=client_id)
        
    except Exception as e:
        messages.error(request, f'Error assigning program: {str(e)}')
        return redirect('trainers:client_calendar', client_id=client_id)

@login_required
def client_programs(request, client_id):
    if request.user.user_type != 'trainer':
        return HttpResponseForbidden('Only trainers can access this page')
    
    client = get_object_or_404(Client, id=client_id, trainer=request.user)
    programs = Program.objects.filter(client=client.user)
    
    return render(request, 'trainers/client_programs.html', {
        'client': client,
        'programs': programs
    })

@login_required
def program_unassign_confirm(request, program_id):
    if request.user.user_type != 'trainer':
        return HttpResponseForbidden('Only trainers can access this page')
    
    program = get_object_or_404(Program, id=program_id, trainer=request.user)
    
    if request.method == 'POST':
        client = program.client
        program.client = None
        program.start_date = None
        program.save()
        messages.success(request, f'Program "{program.name}" has been unassigned from {client.get_full_name()}')
        try:
            client_profile = Client.objects.get(user=client)
            return redirect('trainers:client_programs', client_id=client_profile.id)
        except Client.DoesNotExist:
            messages.error(request, 'Could not find client profile')
            return redirect('trainers:trainer_home')
    
    try:
        client_profile = Client.objects.get(user=program.client)
        return render(request, 'trainers/program_unassign_confirm.html', {
            'program': program,
            'client_profile': client_profile
        })
    except Client.DoesNotExist:
        messages.error(request, 'Could not find client profile')
        return redirect('trainers:trainer_home')

def complete_client_registration(request):
    token = request.GET.get('token')
    if not token:
        messages.error(request, 'Registration token is required')
        return redirect('login')
        
    try:
        registration = ClientRegistrationToken.objects.get(token=token, is_used=False)
    except ClientRegistrationToken.DoesNotExist:
        messages.error(request, 'Invalid or expired registration token')
        return redirect('login')
        
    if request.method == 'POST':
        registration_form = ClientRegistrationForm(request.POST)
        profile_form = ClientProfileForm(request.POST)
        
        if registration_form.is_valid() and profile_form.is_valid():
            # Get the pre-created user
            user = CustomUser.objects.get(email=registration.email)
            
            # Update user details
            user.username = registration_form.cleaned_data['username']
            user.set_password(registration_form.cleaned_data['password1'])
            user.first_name = registration.first_name
            user.last_name = registration.last_name
            user.is_active = True
            user.save()
            
            # Update client profile
            client = Client.objects.get(user=user)
            for field, value in profile_form.cleaned_data.items():
                setattr(client, field, value)
            client.save()
            
            # Mark token as used
            registration.is_used = True
            registration.save()
            
            # Log the user in
            login(request, user)
            
            messages.success(request, 'Your registration is complete! You can now access your account.')
            return redirect('dashboard')
    else:
        registration_form = ClientRegistrationForm()
        profile_form = ClientProfileForm()
    
    return render(request, 'trainers/complete_client_registration.html', {
        'form': registration_form,
        'profile_form': profile_form,
        'token': token
    })

def trainer_register(request):
    if request.method == 'POST':
        form = TrainerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            TrainerProfile.objects.create(trainer=user)
            messages.success(request, 'Your trainer account has been created! You can now log in')
            return redirect('login')
    else:
        form = TrainerRegistrationForm()
    return render(request, 'trainers/trainer_register.html', {'form': form})

@login_required
def register_client(request):
    if request.user.user_type != 'trainer':
        messages.error(request, 'Only trainers can register clients')
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = ClientPreRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            # Check if user already exists
            try:
                client_user = CustomUser.objects.get(email=email)
                if client_user.is_active:
                    messages.error(request, f'User with email {email} already exists and is active')
                    return redirect('trainers:register_client')
                # If user exists but is inactive, we'll reuse it
            except CustomUser.DoesNotExist:
                # Generate a unique username based on email
                import uuid
                base_username = email.split('@')[0]
                username = base_username
                while CustomUser.objects.filter(username=username).exists():
                    # If username exists, append first 8 chars of a UUID
                    username = f"{base_username}_{str(uuid.uuid4())[:8]}"
                
                # Create a new pre-registered client user
                client_user = CustomUser.objects.create(
                    username=username,
                    email=email,
                    user_type='client',
                    is_active=False
                )
                
                try:
                    # Create client profile
                    Client.objects.create(
                        user=client_user,
                        trainer=request.user
                    )
                except Exception as e:
                    # If client profile creation fails, delete the user and show error
                    client_user.delete()
                    messages.error(request, f'Error creating client profile for {email}: {str(e)}')
                    print(f"Client profile creation error: {str(e)}")  # Debug print
                    return redirect('trainers:register_client')

            # Mark any existing tokens for this email as used
            ClientRegistrationToken.objects.filter(email=email).update(is_used=True)
            
            # Create new registration token
            token = ClientRegistrationToken.objects.create(
                email=email,
                trainer=request.user,
                first_name=first_name,
                last_name=last_name
            )
            
            # Send registration email
            token.send_registration_email(request)
            
            messages.success(
                request, 
                f'Registration invitation sent to {email}. They will need to click the link in their email to complete registration.'
            )
            return redirect('dashboard')
    else:
        form = ClientPreRegistrationForm()
    
    # Get all registration tokens created by this trainer
    pending_registrations = ClientRegistrationToken.objects.filter(
        trainer=request.user,
        is_used=False
    ).order_by('-created_at')
    
    return render(request, 'trainers/register_client.html', {
        'form': form,
        'pending_registrations': pending_registrations
    })
