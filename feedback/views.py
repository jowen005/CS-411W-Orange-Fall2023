from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework import status, viewsets

from . import models, serializers, permissions
from restaurants.models import RestrictionTag, AllergyTag, TasteTag, IngredientTag, MenuItem
from restaurants.serializers import MenuItemListSerializer

# Create your views here.

# DO WE WANT front end to submit one API request or 2 every time they want stuff
# So we either consolidate reviews and ratings into one feedback object or make them request twice for everything
