from django.urls import path

from . import viewsets
from .viewsets import drop_cache

urlpatterns = [
    path('deals/',  viewsets.DealsAPIView.as_view(), name='deals'),
    path('deals/<str:cache_key>', viewsets.DealsAPIView.as_view()),
    path('deals/<str:cache_key>/reset', drop_cache),
]

