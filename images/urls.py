from django.urls import path, re_path
from .views import get_image, get_temp_url, list_images, list_routes, upload_image

urlpatterns = [
    path('routes/', list_routes, name='list-routes'),
    path('images/', list_images, name='list-images'),
    path('upload/', upload_image, name='upload-image'),
    path('url/<int:pk>/', get_temp_url, name='get-url'),
    re_path(r'^getimage/\d*\w*$', get_image, name='get-image'),
]
