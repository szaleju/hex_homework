from django.urls import path
from .views import ListImages

urlpatterns = [
    path('images/', ListImages, name='list-images'),
]
