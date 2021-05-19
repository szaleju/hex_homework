from .models import Image, Profile, TempUrl
from .serializers import EnterprisePlanSerializer, BasicPlanSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from datetime import timedelta
from django.utils import timezone


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_images(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    images = Image.objects.filter(user=user)

    if str(profile.plan) == ('enterprise' or 'premium'):
        serializer = EnterprisePlanSerializer(images, many=True)
    else:
        serializer = BasicPlanSerializer(images, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    user = request.user
    image = request.FILES.get('image')
    Image.objects.create()(user=user, original=image)
    Image.save()
    return Response('Image was uploaded')


@api_view(['GET'])
def list_routes(request):
    routes = [
        '/api/images/',
        '/api/upload/'
    ]
    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_temp_url(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    if str(profile.plan) == 'enterprise':
        image = Image.objects.get(id=pk)
        hash = TempUrl.objects.hash_expire_url(image)
        current_site = str(get_current_site(request)) + '/'
        temp_url = 'http://' + current_site + hash
        seconds = int(request.GET.get('seconds'))
        TempUrl.objects.create(
            user=user,
            hash=hash,
            url=temp_url,
            expiry=timezone.now() + timedelta(seconds)
        )
        return Response(temp_url)
    else:
        return Response('Your plan does not allow for link generation.')
