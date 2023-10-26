from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework import status, viewsets

from . import models, serializers, permissions
from restaurants.models import RestrictionTag, AllergyTag, TasteTag, IngredientTag, MenuItem
from restaurants.serializers import MenuItemListSerializer

# Create your views here.

# class ReviewViewSet(viewsets.ModelViewSet):
#     permission_classes = []

#     # def get_queryset(self):
#     #     user = self.request.user
#     #     if user.user_type == 'patron':
#     #         return models.Patron.objects.filter(user=user)
#     #     else:
#     #         return models.Patron.objects.none()
        
#     def get_serializer_class(self):
#         if self.action == 'list' or self.action == 'retrieve':
#             return serializers.ReviewsGetSerializer
#         return serializers.ReviewsSerializer

#     def perform_create(self, serializer):
#         serializer.save(patron=self.request.user)