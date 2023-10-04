from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets

from . import models, serializers, permissions
from restaurants.models import RestrictionTag, AllergyTag, TasteTag


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

@api_view(http_method_names=['GET'])
def tag_overview(request:Request):
    
    patrons =  models.Patron.objects.all()
    allergies = AllergyTag.objects.all()
    restrictions = RestrictionTag.objects.all()
    tastes = TasteTag.objects.all()
    
    response = {"AllergyTag": {},"RestrictionTag":{},"TasteTag":{}}
    for allergy in allergies:
        response["AllergyTag"][str(allergy.id)] = {"title":allergy.title,"count":0}

    for restriction in restrictions:
        response["RestrictionTag"][str(restriction.id)] = {"title":restriction.id, "count":0}

    for taste in tastes:
        response["TasteTag"][str(taste.id)] = {"title":taste.id, "count":0}

    for patron in patrons:
        for tag_id in list(patron.patron_allergy_tag.values_list("id",flat=True)):
            response["AllergyTag"][str(tag_id)]["count"] += 1
        for tag_id in list(patron.patron_restriction_tag.values_list("id",flat=True)):
            response["RestrictionTag"][str(tag_id)]["count"] += 1
        for tag_id in list(patron.patron_taste_tag.values_list("id",flat=True)):
            response["TasteTag"][str(tag_id)]["count"] += 1
        
    return Response(data=response, status=status.HTTP_200_OK)