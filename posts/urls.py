from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('like/<int:id>/', views.post_like, name="like"),
    path('unlike/<int:id>/', views.post_unlike, name="unlike"),
    path('save/<int:id>/', views.post_save, name="save"),
    path('unsave/<int:id>/', views.post_unsave, name="unsave"),
    path('comment/<int:id>/', views.post_comment, name="comment"),
]
