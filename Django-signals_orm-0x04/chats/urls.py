from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    path('', views.conversation_users, name='conversation_users'),
    path('conversation/<int:user_id>/', views.conversation_list, name='conversation_list'),
    path('stats/', views.public_chat_stats, name='public_stats'),
]
