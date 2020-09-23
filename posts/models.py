from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here.


# class PostManager(models.Manager):
#     def get_all_users_who_liked(self, )


class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)
    text_content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=f"posts/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    comments = GenericRelation('Comment', related_query_name='post')
    likes = GenericRelation('Like', related_query_name='post')
    saved = GenericRelation('Saved', related_query_name='post')

    class Meta():
        ordering = ['-created']

    def __str__(self):
        return f"{self.pk}"

    def total_likes(self):
        return self.likes.all().count()

    def get_all_users_who_liked(self):
        users_likes = [like.user for like in self.likes.all()]
        return users_likes

    def get_all_users_who_saved(self):
        saved_posts = []
        for post in self.saved.all():
            saved_posts.append(post.user)
        return saved_posts

    def total_comments(self):
        return self.comments.all().count()


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta():
        ordering = ['-created']

    def __str__(self):
        return self.text


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user}"


class Saved(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user}"
