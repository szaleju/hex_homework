from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, CharField, DateTimeField, URLField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

from io import BytesIO
from django.core.files import File
from PIL import Image as Picture
from hashlib import blake2b


PLAN_STATUS = (
    ('basic', 'Basic'),
    ('premium', 'Premium'),
    ('enterprise', 'Enterprise'),
)


def make_thumbnail(image, size):

    im = Picture.open(image)
    im.convert('RGB')
    im.thumbnail(size)
    thumb_io = BytesIO()
    im.save(thumb_io, 'JPEG', quality=85)
    thumbnail = File(thumb_io, name=image.name)
    return thumbnail


class Plan(models.Model):
    type = CharField(max_length=16, choices=PLAN_STATUS, default='basic')
    thumbnail_s_size = models.PositiveIntegerField()
    thumbnail_m_size = models.PositiveIntegerField(blank=True, null=True)
    create_expire = BooleanField()

    def __str__(self):
        return self.type


class Image(models.Model):
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    original = ImageField(upload_to='images/')
    thumbnail_m = ImageField(
        upload_to='images/thumbnails/m/', blank=True, null=True)
    thumbnail_s = ImageField(
        upload_to='images/thumbnails/s/', blank=True, null=True)

    def __str__(self):
        return str(self.original.url)

    def save(self, *args, **kwargs):
        self.thumbnail_s = make_thumbnail(self.original, (200, 200))
        self.thumbnail_m = make_thumbnail(self.original, (400, 400))
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    plan = ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class TempUrlManager(models.Manager):

    def hash_expire_url(self, obj):

        key = bytes(str(timezone.now()), 'utf-8')
        hash = blake2b(digest_size=16, key=key)
        original_url = bytes(obj.original.url, 'utf-8')
        hash.update(original_url)
        return hash.hexdigest()


class TempUrl(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    hash = CharField(max_length=32)
    url = URLField()
    created_at = DateTimeField(auto_now_add=True)
    expiry = DateTimeField()
    objects = TempUrlManager()

    def verify(self):
        return timezone.now() < self.expiry
