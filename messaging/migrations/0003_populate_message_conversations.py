from django.db import migrations
from django.db.models import Q

def create_conversations(apps, schema_editor):
    Message = apps.get_model('messaging', 'Message')
    Conversation = apps.get_model('messaging', 'Conversation')
    
    # Get all unique sender-recipient pairs
    messages = Message.objects.all()
    conversation_pairs = set()
    
    for message in messages:
        # Sort user IDs to ensure consistent pairing
        pair = tuple(sorted([message.sender_id, message.recipient_id]))
        conversation_pairs.add(pair)
    
    # Create conversations for each pair and update messages
    for user1_id, user2_id in conversation_pairs:
        # Create conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(user1_id, user2_id)
        
        # Update all messages between these users
        Message.objects.filter(
            Q(sender_id=user1_id, recipient_id=user2_id) |
            Q(sender_id=user2_id, recipient_id=user1_id)
        ).update(conversation=conversation)

def reverse_conversations(apps, schema_editor):
    Message = apps.get_model('messaging', 'Message')
    Conversation = apps.get_model('messaging', 'Conversation')
    
    # Clear conversation references from messages
    Message.objects.all().update(conversation=None)
    # Delete all conversations
    Conversation.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_message_conversation'),
    ]

    operations = [
        migrations.RunPython(create_conversations, reverse_conversations),
    ]
