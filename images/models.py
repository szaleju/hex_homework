from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, CharField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey

PLAN_STATUS = (
    ('basic', 'Basic'),
    ('premium', 'Premium'),
    ('enterprise', 'Enterprise'),
)


class Plan(models.Model):
    type = CharField(max_length=16, choices=PLAN_STATUS, default='basic')
    thumbnail_s_size = models.PositiveIntegerField()
    thumbnail_m_size = models.PositiveIntegerField(blank=True, null=True)
    create_expire = BooleanField()

    def __str__(self):
        return self.type


class Image(models.Model):
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    original = ImageField()
    thumbnail_m = ImageField(
        upload_to='images/thumbnails/m', blank=True, null=True)
    thumbnail_s = ImageField(
        upload_to='images/thumbnails/s', blank=True, null=True)

    def __str__(self):
        return str(self.original.url)


class Profile(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    plan = ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
