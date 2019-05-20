from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.timezone import now


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    notification = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


class SportActivity(models.Model):
    activity_name = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=1000, default='')
    time = models.DurationField()

    def __str__(self):
        return self.activity_name


post_save.connect(create_profile, sender=User)


class Dish(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class Product(models.Model):
    name_product = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1000, default='')
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name_product


class Tip(models.Model):
    tip = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.tip


class TipStudy(models.Model):
    tip = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.tip


class SportActivityNotification(models.Model):
    activity_name = models.CharField(max_length=50, default='')
    link = models.ForeignKey(User, related_name='sportactivitynotifications',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.activity_name



