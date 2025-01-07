from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Message, Conversation, Forum, ForumMessage
from .forms import MessageForm, ForumForm, ForumMessageForm, ForumParticipantForm

@login_required
def conversation_list(request):
    conversations = request.user.conversations.all()
    return render(request, 'messaging/conversation_list.html', {
        'conversations': conversations
    })

@login_required
def start_conversation(request, user_id):
    recipient = get_object_or_404(get_user_model(), id=user_id)
    
    # Check if conversation already exists
    existing_conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=recipient
    ).first()
    
    if existing_conversation:
        return redirect('messaging:conversation_detail', pk=existing_conversation.pk)
    
    # Create new conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, recipient)
    
    return redirect('messaging:conversation_detail', pk=conversation.pk)

@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in conversation.participants.all():
        raise PermissionDenied
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.recipient = conversation.get_other_participant(request.user)
            message.save()
            return redirect('messaging:conversation_detail', pk=pk)
    else:
        form = MessageForm()
    
    messages_list = conversation.messages.all()
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages_list,
        'form': form
    })

@login_required
def forum_list(request):
    # Show forums where user is either trainer or participant
    forums = Forum.objects.filter(
        Q(trainer=request.user) | Q(participants=request.user)
    ).distinct()
    
    # Only trainers can create forums
    form = ForumForm(trainer=request.user) if request.user.is_trainer else None
    
    if request.method == 'POST':
        if not request.user.is_trainer:
            raise PermissionDenied
        form = ForumForm(request.POST, trainer=request.user)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.trainer = request.user  # Explicitly set the trainer
            forum.save()
            form.save_m2m()  # Save the many-to-many relationships
            messages.success(request, 'Forum created successfully.')
            return redirect('messaging:forum_detail', pk=forum.pk)
    
    return render(request, 'messaging/forum_list.html', {
        'forums': forums,
        'form': form
    })

@login_required
def forum_detail(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    # Allow access if user is either the trainer or a participant
    if request.user != forum.trainer and request.user not in forum.participants.all():
        raise PermissionDenied
    
    if request.method == 'POST':
        form = ForumMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.forum = forum
            message.sender = request.user
            message.clean()  # Validate after setting forum and sender
            message.save()
            return redirect('messaging:forum_detail', pk=pk)
    else:
        form = ForumMessageForm()
    
    # Only trainer can see participant management form
    participant_form = None
    if request.user == forum.trainer:
        participant_form = ForumParticipantForm(trainer=request.user, forum=forum)
    
    messages_list = forum.messages.all()
    return render(request, 'messaging/forum_detail.html', {
        'forum': forum,
        'messages': messages_list,
        'form': form,
        'participant_form': participant_form
    })

@login_required
def manage_forum_participants(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    if request.user != forum.trainer:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = ForumParticipantForm(request.POST, trainer=request.user, forum=forum)
        if form.is_valid():
            new_participants = form.cleaned_data['participants']
            forum.participants.add(*new_participants)
            messages.success(request, 'Participants added successfully.')
            return redirect('messaging:forum_detail', pk=pk)
    
    return redirect('messaging:forum_detail', pk=pk)

@login_required
def remove_forum_participant(request, forum_pk, user_pk):
    forum = get_object_or_404(Forum, pk=forum_pk)
    if request.user != forum.trainer:
        raise PermissionDenied
    
    if request.method == 'POST':
        participant = get_object_or_404(get_user_model(), pk=user_pk)
        if participant != forum.trainer:  # Can't remove the trainer
            forum.participants.remove(participant)
            messages.success(request, f'{participant.get_full_name()} removed from forum.')
    
    return redirect('messaging:forum_detail', pk=forum_pk)
