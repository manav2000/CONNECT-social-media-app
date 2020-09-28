from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.home_view, name="home"),
    path('like/', views.post_like, name="like"),
    path('save/', views.post_save, name="save"),
    path('comment/', views.post_comment, name="comment"),
    path('delete/', views.post_delete, name="delete"),
]
