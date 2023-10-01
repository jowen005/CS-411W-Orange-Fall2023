from rest_framework import viewsets

from . import models, serializers, permissions


# Create your views here.

class PatronViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PatronSerializer
    permission_classes = [permissions.IsAuthPatronAndIsUser]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patron':
            return models.Patron.objects.filter(user=user)
        else:
            return models.Patron.objects.none()
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)