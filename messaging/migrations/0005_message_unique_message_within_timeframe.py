# Generated by Django 4.2.7 on 2025-01-05 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0004_alter_message_conversation'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='message',
            constraint=models.UniqueConstraint(fields=('sender', 'recipient', 'conversation', 'text_content', 'timestamp'), name='unique_message_within_timeframe'),
        ),
    ]
