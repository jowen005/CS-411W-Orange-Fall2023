from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register("", views.RestTagViewSet, basename="resttags")


urlpatterns = [
    path('handshake/', views.handshake, name='handshake'),
    path('resttags/', include(router.urls))
]