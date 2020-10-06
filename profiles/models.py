from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models import Q


from connect.storage_backends import PublicMediaStorage


# Create your models here.

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
    ('Perfer Not To Say', 'Perfer Not To Say')
)


class ProfileManager(models.Manager):
    def get_all_profiles(self, me):
        return Profile.objects.all().exclude(user=me)

    def get_saved_posts(self, me, post_class):
        saved_posts_ids = [post.object_id for post in me.saved_set.all()]
        saved_posts = post_class.objects.filter(id__in=saved_posts_ids)
        return saved_posts


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(choices=GENDER, blank=True, max_length=25)
    country = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}"

    @property
    def get_username(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        slug_text = f"{self.user.username}"
        self.slug = slugify(slug_text)
        return super(Profile, self).save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def get_all_request_by_me(self, me):
        return Relationship.objects.filter(sender=me, status='send').only('receiver')

    def get_all_followers(self, receiver):
        return Relationship.objects.filter(receiver=receiver, status='accepted').only('sender')

    def get_all_following(self, sender):
        return Relationship.objects.filter(sender=sender, status='accepted').only('receiver')

    def get_all_friends(self, me):
        all_friends = Relationship.objects.filter(
            (Q(sender=me) | Q(receiver=me)) & Q(status='accepted')).only('sender', 'receiver')
        friends_profiles = []
        for friend in all_friends:
            if friend.sender == me:
                friends_profiles.append(friend.receiver)
            else:
                friends_profiles.append(friend.sender)
        return list(set(friends_profiles))


class Relationship(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender.user.username} - {self.receiver.user.username} - {self.status} - {self.created}"
