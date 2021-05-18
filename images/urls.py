from django.urls import path
from .views import list_images, list_routes, upload_image

urlpatterns = [
    path('routes/', list_routes, name='list-routes'),
    path('images/', list_images, name='list-images'),
    path('upload/', upload_image, name='upload-image')
]
