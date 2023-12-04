from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('satisfaction', views.AppSatisfactionTrendsViewset, basename='satisfaction')

filter_router = DefaultRouter()
filter_router.register('', views.FilterTrendsViewset, basename='filter')

menu_router = DefaultRouter()
menu_router.register('menuitems', views.MenuItemPerformanceTrendsViewset, basename='localmenuitems')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:restaurant_id>/', include(menu_router.urls)),
    path('<str:filter_type>/', include(filter_router.urls)),
]
