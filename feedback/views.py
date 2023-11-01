from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework import status, viewsets

from . import models, serializers, permissions
from restaurants.models import MenuItem
from restaurants.serializers import MenuItemListSerializer

# Create your views here.

class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.FeedbackPermission]

    def get_queryset(self):
        
        user = self.request.user

        # queries for reviews for a specified menu item
        if self.action == 'list':
            menu_item = MenuItem.objects.get(id=self.request.data['menu_item'])
            return models.Reviews.objects.filter(menu_item=menu_item)
        
        # queries for reviews for a specific patron
        elif user.user_type == 'patron':
            return models.Reviews.objects.filter(patron=user)
        
        else:
            return models.Reviews.objects.none()
        
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.ReviewsGetSerializer
        return serializers.ReviewsSerializer

    def perform_create(self, serializer):
        serializer.save(patron=self.request.user)