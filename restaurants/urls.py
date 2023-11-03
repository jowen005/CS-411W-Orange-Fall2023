from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('resttags', views.RestTagViewSet, basename='resttags')
router.register('foodtypetags', views.FoodTypeTagViewSet, basename='foodtypetags')
router.register('cookstyletags', views.CookStyleTagViewSet, basename='cookstyletags')
router.register('tastetags', views.TasteTagViewSet, basename='tastetags')
router.register('restrictiontags', views.RestrictionTagViewSet, basename='restrictiontags')
router.register('allergytags', views.AllergyTagViewSet, basename='allergytags')
router.register('ingredienttags', views.IngredientTagViewSet, basename='ingredienttags')


#Must go last
router.register('', views.RestaurantViewSet, basename='restaurants')

menu_router = DefaultRouter()
menu_router.register('menuitems', views.MenuItemViewSet, basename='menuitems')


urlpatterns = [
    path('handshake/', views.handshake, name='handshake'),
    path('', include(router.urls)),
    path('menuitems/<int:pk>/', views.MenuItemRetrieveAPIView.as_view(), name='menuitems-retrieve'),
    path('<int:restaurant_id>/', include(menu_router.urls))
]

# urlpatterns += router.urls