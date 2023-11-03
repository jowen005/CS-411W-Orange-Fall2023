from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets, generics

from . import models, serializers, permissions

# Create your views here.

class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [permissions.IsAuthRestAndIsOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'restaurant':
            return models.Restaurant.objects.filter(owner=user)
        else:
            return models.Restaurant.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RestaurantListSerializer
        if self.action == 'retrieve':
            return serializers.RestaurantGetSerializer
        return serializers.RestaurantSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [permissions.MenuItemPermission]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'restaurant':
            requested_id = self.kwargs.get('restaurant_id')
            restaurant = models.Restaurant.objects.get(pk=requested_id)
            return models.MenuItem.objects.filter(restaurant=restaurant)
        # elif user.user_type == 'patron' or user.user_type == 'admin':
        #     return models.MenuItem.objects.all()
        else:
            return models.Restaurant.objects.none()

    def perform_create(self, serializer):
        requested_id = self.kwargs.get('restaurant_id')
        restaurant = models.Restaurant.objects.get(pk=requested_id)
        serializer.save(restaurant=restaurant)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MenuItemListSerializer
        if self.action == 'retrieve':
            return serializers.MenuItemGetSerializer
        return serializers.MenuItemSerializer


class MenuItemRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemGetSerializer
    permission_classes = [permissions.IsAuth]


class RestTagViewSet(viewsets.ModelViewSet):
    queryset = models.RestTag.objects.all()
    serializer_class = serializers.RestTagSerializer
    permission_classes = [permissions.IsAdminOrAuthReadOnly]


class FoodTypeTagViewSet(viewsets.ModelViewSet):
    queryset = models.FoodTypeTag.objects.all()
    serializer_class = serializers.FoodTypeTagSerializer
    permission_classes = [permissions.IsAdminOrAuthReadOnly]


class CookStyleTagViewSet(viewsets.ModelViewSet):
    queryset = models.CookStyleTag.objects.all()
    serializer_class = serializers.CookStyleTagSerializer
    permission_classes = [permissions.IsAdminOrAuthReadOnly]


class TasteTagViewSet(viewsets.ModelViewSet):
    queryset = models.TasteTag.objects.all()
    serializer_class = serializers.TasteTagSerializer
    permission_classes = [permissions.IsAdminOrAuthReadOnly]


class RestrictionTagViewSet(viewsets.ModelViewSet):
    queryset = models.RestrictionTag.objects.all()
    serializer_class = serializers.RestrictionTagSerializer
    permission_classes = [permissions.IsAdminOrAuthReadOnly]


class AllergyTagViewSet(viewsets.ModelViewSet):
    queryset = models.AllergyTag.objects.all()
    serializer_class = serializers.AllergyTagSerializer
    permission_classes = [permissions.IsAdminOrAuthReadOnly]


class IngredientTagViewSet(viewsets.ModelViewSet):
    queryset = models.IngredientTag.objects.all()
    serializer_class = serializers.IngredientTagSerializer
    permission_classes = [permissions.IsAdminOrAuthReadOnly]


@api_view(http_method_names=['GET'])
def handshake(request:Request):
    response = {
        'message': 'This API handshake was successful',
        'content': 'Hello World! This is a Dev Branch'
    }
    return Response(data=response, status=status.HTTP_200_OK)

