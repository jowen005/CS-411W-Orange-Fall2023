from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, views
from django.core.management import call_command

from . import models, serializers, permissions
import restaurants.models as rm


class FilterTrendsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsNonPatronRetrieveAndValidFilter]

    # filter_type: (Serializer, TrendsModel, TagModel)
    FILTER_MODELS = {
        'calories': (serializers.CalorieTrendsSerializer, models.CalorieTrends, None),
        'restrictiontag': (serializers.RestrictionTagTrendsSerializer, models.RestrictionTagTrends, rm.RestrictionTag),
        'allergytag': (serializers.AllergyTagTrendsSerializer, models.AllergyTagTrends, rm.AllergyTag),
        'ingredienttag': (serializers.IngredientTagTrendsSerializer, models.IngredientTagTrends, rm.IngredientTag),
        'tastetag': (serializers.TasteTagTrendsSerializer, models.TasteTagTrends, rm.TasteTag),
        'cookstyletag': (serializers.CookStyleTagTrendsSerializer, models.CookStyleTagTrends, rm.CookStyleTag)
    }
    
    def get_serializer_class(self):
        filter_type = self.kwargs.get('filter_type')
        return self.FILTER_MODELS[filter_type][0]

    def get_queryset(self):
        filter_type = self.kwargs.get('filter_type')
        TrendsModel = self.FILTER_MODELS[filter_type][1]

        # Get id_attr
        if filter_type == 'calories':
            id_attr = 'calorie_level'
        else:
            id_attr = 'tag__id'

        try:
            latest_datestamp = TrendsModel.objects.latest('date_stamp').date_stamp
        except TrendsModel.DoesNotExist:
            return TrendsModel.objects.none()

        queryset = TrendsModel.objects.filter(
            date_stamp=latest_datestamp
        ).order_by(id_attr)

        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        filter_type = self.kwargs.get('filter_type')
        tag_id = int(kwargs.get('pk'))
        TagModel = self.FILTER_MODELS[filter_type][2]

        # Validate PK Input
        if TagModel == None:    # Calories
            id_attr = 'calorie_level'
            if tag_id < 1 or tag_id > 11:
                response = {
                    'message': 'Supplied Calorie Level must be ' +
                               'within the range 1 to 11 inclusive!'
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        else:
            id_attr = 'tag__id'
            try:
                TagModel.objects.get(id=tag_id)
            except TagModel.DoesNotExist:
                response = {
                    'message': f'This Tag ID ({tag_id}) is not valid!'
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()
        trend_objs = queryset.filter(**{id_attr: tag_id})
        if trend_objs.count() != 2:
            response = {
                'message': f'This Tag ID or Calorie Level ({tag_id}) is valid but does not yet have all analytics!'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(trend_objs, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class MenuItemPerformanceTrendsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.LocalMenuItemTrendPermission]
    serializer_class = serializers.MenuItemPerformanceTrendsSerializer

    def get_queryset(self):
        requested_id = self.kwargs.get('restaurant_id')

        try:
            latest_datestamp = models.MenuItemPerformanceTrends.objects.filter(
                item__restaurant__id=requested_id
            ).latest('date_stamp').date_stamp
        except models.MenuItemPerformanceTrends.DoesNotExist:
            return models.MenuItemPerformanceTrends.objects.none()
        
        queryset = models.MenuItemPerformanceTrends.objects.filter(
            item__restaurant__id=requested_id,
            date_stamp=latest_datestamp
        ).order_by('item__id')

        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        item_id = int(kwargs.get('pk'))

        # PK Input is Validated in the permission

        queryset = self.get_queryset()
        trend_objs = queryset.filter(item__id=item_id)
        if trend_objs.count() != 3:
            response = {
                'message': f'This Menu Item ({item_id}) is valid but does not yet have all analytics!'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(trend_objs, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
        

class AppSatisfactionTrendsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAdminAndList]
    serializer_class = serializers.AppSatisfactionTrendsSerializer

    def get_queryset(self):
        try:
            latest_datestamp = models.AppSatisfactionTrends.objects.latest('date_stamp').date_stamp
        except models.AppSatisfactionTrends.DoesNotExist:
            return models.AppSatisfactionTrends.objects.none()
        
        queryset = models.AppSatisfactionTrends.objects.filter(
            date_stamp=latest_datestamp
        )

        return queryset
    

class ManualTrendsCommandView(views.APIView):
    permission_classes = [permissions.IsAuthAdminAndCreate]

    def post(self, request, *args, **kwargs):
        call_command('manualTrends')

        return Response({'detail':'manualTrends was triggered successfully.'}, status=status.HTTP_200_OK)

