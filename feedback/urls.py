from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Does the url routing for PatronViewSet
router = DefaultRouter()
router.register('', views.ReviewViewSet, basename='feedback')


urlpatterns = [
    # path('tag_overview/', views.tag_overview, name='analytics'),
    path('', include(router.urls))
    
]