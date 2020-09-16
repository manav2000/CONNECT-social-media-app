from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<str:slug>/', views.user_profile_detail_view,
         name="profile-detail-view"),
]
