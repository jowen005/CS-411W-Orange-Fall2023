from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Does the url routing for PatronViewSet
router = DefaultRouter()
router.register('searchhistory', views.SearchHistoryViewSet, basename='searchhistory')
router.register('bookmarks', views.BookmarkViewSet, basename='bookmark')
router.register('menuitemhistory', views.MenuItemHistoryViewSet, basename='menuitemhistory')
router.register('', views.PatronViewSet, basename='patron')


urlpatterns = [
    path('', include(router.urls))
    
]