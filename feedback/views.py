from rest_framework.response import Response
from rest_framework import status, viewsets, generics

from . import models, serializers, permissions
from restaurants.models import MenuItem


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.FeedbackPermission]

    def get_queryset(self):
        
        user = self.request.user
        
        # queries for reviews for a specific patron
        if user.user_type == 'patron':
            return models.Reviews.objects.filter(patron=user)
        else:
            return models.Reviews.objects.none()
        
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ReviewsGetSerializer
        return serializers.ReviewsSerializer

    def perform_create(self, serializer):
        serializer.save(patron=self.request.user)


class RetrieveMenuItemReviewsAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuth]
    serializer_class = serializers.ReviewsGetSerializer
    queryset = models.Reviews.objects.all()

    def retrieve(self, request, *args, **kwargs):
        item_id = int(kwargs.get('pk'))

        # Validate PK Input
        try:
            MenuItem.objects.get(id=item_id)
        except MenuItem.DoesNotExist:
            response = {
                'message': f'This Menu Item ID ({item_id}) is not valid!'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()
        reviews = queryset.filter(menu_item__id=item_id).order_by('-review_datetime')

        serializer = self.get_serializer(reviews, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AppSatisfactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AdminReadNonAdminWrite]
    serializer_class = serializers.AppSatisfactionSerializer
    queryset = models.AppSatisfaction.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

