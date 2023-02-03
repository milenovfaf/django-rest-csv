from django.urls import path

from . import viewsets

urlpatterns = [
    path('deals/',  viewsets.DealsAPIView.as_view(), name='deals'),
]

