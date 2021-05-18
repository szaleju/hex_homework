from rest_framework import serializers
from .models import Image


class BasicPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['thumbnail_s']


class PremiumPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['original', 'thumbnail_m', 'thumbnail_s']


class EnterprisePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['original', 'thumbnail_m', 'thumbnail_s', ]
