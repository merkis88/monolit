from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import default
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='image_question/', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_duration = models.PositiveIntegerField(default=1)

    def is_expired(self):
        return timezone.now() > (self.created_at + timedelta(days=self.valid_duration))

    def __str__(self):
        return self.title
class AnswerOption(models.Model):
    post = models.ForeignKey(Post, related_name='answer_options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='votes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

# Create your models here.
