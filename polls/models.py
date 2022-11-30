import datetime

from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=datetime.datetime.today())
    close_date = models.DateTimeField('date closed', default=datetime.datetime.today() + datetime.timedelta(hours=1))
    short_description = models.CharField(max_length=1000, default='')
    long_description = models.CharField(max_length=10000, default='')
    image = models.ImageField(default='',blank=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(hours=1)

    @property
    def is_past_due(self):
        return datetime.datetime.today() > datetime.datetime(self.close_date.year, self.close_date.month, self.close_date.day, self.close_date.hour, self.close_date.minute, self.close_date.second)


    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    percent = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='non.png')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class UserVote(models.Model):
    question = models.IntegerField()
    user_id = models.IntegerField()

