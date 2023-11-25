from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Does the url routing for PatronViewSet
router = DefaultRouter()
router.register('global', views.GlobalAnalyticsViewset, basename='global')
router.register('calories', views.CalorieAnalyticsViewset, basename='calories')
router.register('restrictiontag', views.RestrictionTagAnalyticsViewset, basename='restrictiontag')
router.register('allergytag', views.AllergiesTagAnalyticsViewset, basename='allergytag')
router.register('ingredienttag', views.IngredientTagAnalyticsViewset, basename='ingredienttag')
router.register('tastetag', views.TasteTagAnalyticsViewset, basename='tastetag')
router.register('menuitems', views.GlobalMenuItemPerformanceViewset, basename='globalmenuitems')
router.register('satisfaction', views.AppSatisfactionAnalyticsViewset, basename='satisfaction')

menu_router = DefaultRouter()
router.register('menuitems', views.LocalMenuItemPerformanceViewset, basename='localmenuitems')

urlpatterns = [
    # path('tag_overview/', views.tag_overview, name='analytics'),
    path('', include(router.urls)),
    path('<int:restaurant_id>/', include(menu_router.urls))
    
]