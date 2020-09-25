from django.urls import path
from . import views

app_name = 'chat'


urlpatterns = [
    path('friends/', views.friends_list_to_chat, name='friends-list'),
    path('<str:username>/', views.ThreadView.as_view(), name="chat-room"),
]
