from .models import Image, Profile, TempUrl
from .serializers import EnterprisePlanSerializer, BasicPlanSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from datetime import timedelta
from django.utils import timezone
from django.http import FileResponse


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
        'AUTHENTICATION REQUIRED',
        '/api/images/   # List user images',
        '/api/upload/   # Upload an image',
        '/url/<int:pk>/ # Generate link with expire access for an image',
    ]
    return Response(routes)


def make_temp_url(request, hash):
    current_site = str(get_current_site(request)) + '/'
    return 'http://' + current_site + 'api/getimage/' + hash


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_temp_url(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    seconds = int(request.GET.get('seconds'))
    if str(profile.plan) == 'enterprise' and 300 <= seconds <= 3000:
        image = Image.objects.get(id=pk)
        hash = TempUrl.objects.hash_expire_url(image)
        expiry = timezone.now() + timedelta(seconds=seconds)
        TempUrl.objects.create(
            user=user,
            image=image,
            hash=hash,
            expiry=expiry,
        )
        return Response(make_temp_url(request, hash))
    else:
        return Response('Number of seconds must be between 300 and 3000 or you have wrong plan.')


@api_view(['GET'])
def get_image(request):
    path = str(request.get_full_path())
    hash = path.split('/')[-1]
    try:
        temp_url = TempUrl.objects.get(hash=hash)
        if temp_url.verify():
            image = temp_url.image
            return FileResponse(image.original)
        else:
            return Response('Your link expired.')
    except TempUrl.DoesNotExist:
        return Response('Your link is invalid.')
