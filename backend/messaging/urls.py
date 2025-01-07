from django.urls import path
from . import views

app_name = 'messaging'  # Add namespace

urlpatterns = [
    # Conversation URLs
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('start-conversation/<int:user_id>/', views.start_conversation, name='start_conversation'),
    
    # Forum URLs
    path('forums/', views.forum_list, name='forum_list'),
    path('forums/<int:pk>/', views.forum_detail, name='forum_detail'),
    path('forums/<int:pk>/participants/', views.manage_forum_participants, name='manage_forum_participants'),
    path('forums/<int:forum_pk>/participants/<int:user_pk>/remove/', views.remove_forum_participant, name='remove_forum_participant'),
]
