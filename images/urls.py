from django.urls import path
from .views import list_images, upload_image

urlpatterns = [
    path('images/', list_images, name='list-images'),
    path('upload/', upload_image, name='upload-image')
]
