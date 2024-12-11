from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'rent', views.RentViewSet, basename='rent')

urlpatterns = [
    path('', include(router.urls)),
]
