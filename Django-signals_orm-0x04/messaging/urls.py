from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('send/', views.send_message, name='send_message'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('notifications/', views.notifications, name='notifications'),
    path('delete-account/', views.delete_user_account, name='delete_account'),
    path('api/unread-count/', views.api_unread_count, name='api_unread_count'),
]
