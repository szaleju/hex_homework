from django.shortcuts import render
from .models import Image, Profile
from .serializers import EnterprisePlanSerializer, BasicPlanSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def ListImages(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    images = Image.objects.filter(user=user)

    if str(profile.plan) == ('enterprise' or 'premium'):
        serializer = EnterprisePlanSerializer(images, many=True)
    else:
        serializer = BasicPlanSerializer(images, many=True)
    return Response(serializer.data)
