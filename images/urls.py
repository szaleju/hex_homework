from django.urls import path, include
from .views import ListImages

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('images/', ListImages, name='list-images'),
]
