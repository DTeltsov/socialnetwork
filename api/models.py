from datetime import datetime

from django.db.models import Count
from django.db import models
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    test = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_username(self):
        return self.user.username


class Post(models.Model):
    text = models.CharField(max_length=200)
    posted_by = CurrentUserField(related_name='posted_by')
    pub_date = models.DateTimeField('Publication Date', auto_now=True)


    def get_likes_analitics(self, date_to=None, date_from=None):
        if date_from is None and date_to is None:
            return PostRate.objects.filter(liked=True, rated_post=self).values('rate_date').annotate(likes_count=Count('id'))
        elif date_from is not None and date_to is None:
            return PostRate.objects.filter(liked=True, rated_post=self, rate_date__range=[date_from,datetime.now()]).values('rate_date').annotate(likes_count=Count('id'))
        elif date_from is None and date_to is not None:
            postrate = PostRate.objects.filter(liked=True, rated_post=self).order_by('rate_date').first()
            return PostRate.objects.filter(liked=True, rated_post=self, rate_date__range=[postrate.rate_date, date_to]).values('rate_date').annotate(likes_count=Count('id'))
        else:
            return PostRate.objects.filter(liked=True, rated_post=self, rate_date__range=[date_from,date_to]).values('rate_date').annotate(likes_count=Count('id'))


    def get_likes_count(self):
        return PostRate.objects.filter(liked=True, rated_post=self).count()


    def __str__(self):
        return self.text


class PostRate(models.Model):
    liked = models.BooleanField(null=True)
    rated_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rate_date = models.DateField(auto_now=True)
    

    def __str__(self):
        return str(self.rated_post) + ' ' + str(self.rated_by.username)


class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(default=datetime.now())


    def get_last_login(self):
        user = User.objects.get(id=self.user.id)
        return user.last_login
