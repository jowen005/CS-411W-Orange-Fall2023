from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('resttags', views.RestTagViewSet, basename='resttags')
router.register('foodtypetags', views.FoodTypeTagViewSet, basename='foodtypetags')
router.register('cookstyletags', views.CookStyleTagViewSet, basename='cookstyletags')
router.register('tastetags', views.TasteTagViewSet, basename='tastetags')
router.register('', views.RestaurantViewSet, basename='restaurants')


urlpatterns = [
    path('handshake', views.handshake, name='handshake'),
    path('', include(router.urls))
]

# urlpatterns += router.urls