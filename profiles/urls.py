from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<str:slug>/', views.user_profile_detail_view,
         name="profile-detail-view"),
    path('follow/<str:slug>/', views.user_follow, name="user-follow"),
    path('unfollow/<str:slug>/', views.user_unfollow, name="user-unfollow"),
    path('confirm/<str:slug>/', views.confirm_follow_request, name="confirm-request"),
    path('delete/<str:slug>/', views.delete_follow_request, name="delete-request"),
]
