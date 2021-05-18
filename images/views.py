from django.shortcuts import render
from .models import Image
from .serializers import ImageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def ListImages(request):
    user = request.user
    images = Image.objects.filter(user=user)
    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data)
