from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Does the url routing for PatronViewSet
router = DefaultRouter()
router.register('global', views.GlobalAnalyticsViewset, basename='global')
router.register('login', views.LoginAnalyticsViewset, basename='login')
router.register('calories', views.CalorieAnalyticsViewset, basename='calories')
router.register('restrictiontag', views.RestrictionTagAnalyticsViewset, basename='restrictiontag')
router.register('allergytag', views.AllergiesTagAnalyticsViewset, basename='allergytag')
router.register('ingredienttag', views.IngredientTagAnalyticsViewset, basename='ingredienttag')
router.register('tastetag', views.TasteTagAnalyticsViewset, basename='tastetag')
router.register('cookstyletag', views.CookStyleAnalyticsViewset, basename='cookstyletag')
router.register('menuitems', views.GlobalMenuItemPerformanceViewset, basename='globalmenuitems')
router.register('satisfaction', views.AppSatisfactionAnalyticsViewset, basename='satisfaction')

menu_router = DefaultRouter()
menu_router.register('menuitems', views.LocalMenuItemPerformanceViewset, basename='localmenuitems')
menu_router.register('overall', views.LocalRestaurantAnalyticsViewset, basename='overallrest')

urlpatterns = [
    # path('tag_overview/', views.tag_overview, name='analytics'),
    path('', include(router.urls)),
    path('<int:restaurant_id>/', include(menu_router.urls)),
    path('manual/', views.ManualAnalyticsCommandView.as_view(), name='manual'),
    path('overall/login/', views.OverallLoginAnalyticsView.as_view(), name='overalllogins'),
    path('overall/<str:filter_type>/', views.OverallFilterAnalyticsViewset.as_view({'get':'list'}), name='overallfilters'),
    
]