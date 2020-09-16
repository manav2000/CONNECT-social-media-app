from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse

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

    # def get_user_profile(self, request):
    #     user_obj = User.objects.get(username=request.user)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(choices=GENDER, blank=True, max_length=25)
    country = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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
    def get_all_follow_requests(self, receiver):
        p = Profile.objects.get(user=receiver)
        return Relationship.objects.filter(receiver=p, status='send')

    def get_all_followers(self, receiver):
        p = Profile.objects.get(user=receiver)
        return Relationship.objects.filter(receiver=p, status='accepted')

    def get_all_following(self, sender):
        p = Profile.objects.get(user=sender)
        return Relationship.objects.filter(sender=p, status='accepted')


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
