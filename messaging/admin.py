from django.contrib import admin
from .models import Message, Conversation, Forum, ForumMessage

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'text_content', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('text_content', 'sender__username', 'recipient__username')
    date_hierarchy = 'timestamp'

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'last_message')
    filter_horizontal = ('participants',)
    search_fields = ('participants__username',)
    date_hierarchy = 'last_message'

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer', 'created_at', 'last_activity')
    list_filter = ('created_at', 'last_activity')
    search_fields = ('name', 'description', 'trainer__username')
    filter_horizontal = ('participants',)
    date_hierarchy = 'created_at'

@admin.register(ForumMessage)
class ForumMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'forum', 'text_content', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('text_content', 'sender__username', 'forum__name')
    date_hierarchy = 'timestamp'
