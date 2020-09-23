from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('like/', views.post_like, name="like"),
    path('save/<int:id>/', views.post_save, name="save"),
    path('unsave/<int:id>/', views.post_unsave, name="unsave"),
    path('comment/', views.post_comment, name="comment"),
]
