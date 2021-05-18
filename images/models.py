from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, CharField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField

PLAN_STATUS = {
    ('basic', 'Basic'),
    ('premium', 'Premium'),
    ('enterprise', 'Enterprise'),
}


class Plan(models.Model):
    type = CharField(max_length=16, choices=PLAN_STATUS, default='basic')
    thumbnail_s_size = models.PositiveIntegerField()
    thumbnail_m_size = models.PositiveIntegerField()
    create_expire = BooleanField()


class Image(models.Model):
    original = ImageField()
    thumbnail_m = ImageField(upload_to='images/thumbnails/m')
    thumbnail_s = ImageField(upload_to='images/thumbnails/s')


class Profile(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    plan = ForeignKey(Plan, on_delete=models.CASCADE)
    images = ManyToManyField(Image)
