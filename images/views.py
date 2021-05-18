from .models import Image, Profile
from .serializers import EnterprisePlanSerializer, BasicPlanSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
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
