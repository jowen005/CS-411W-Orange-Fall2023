from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets, generics, mixins

from . import models, serializers, permissions

# Create your views here.

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


@api_view(http_method_names=['GET'])
def handshake(request:Request):
    response = {
        'message': 'This API handshake was successful',
        'content': 'Hello World! This is a Dev Branch'
    }
    return Response(data=response, status=status.HTTP_200_OK)

