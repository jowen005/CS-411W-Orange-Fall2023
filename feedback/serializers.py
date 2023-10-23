from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from restaurants.models import MenuItem


User = get_user_model()

# Serializer for Reviews model
class ReviewsSerializer(serializers.ModelSerializer):
    # Uncommenting Patron may work
    #patron = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    patron_review = serializers.CharField(max_length=255,null=True)
    review_datetime = serializers.DateTimeField(auto_now_add=True)

    class Meta:
        model = models.Reviews
        fields = '__all__'
        read_only_fields = ['patron']

    # def formatted_datetime(self):
    #     return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')

#Serializer for Ratings model    
class RatingsSerializer(serializers.ModelSerializer):
    #patron = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    
    #Does this need to be a choice field?
    ratings = serializers.IntegerField(
        choices = [('1', '1'), ('2', '2'), ('3', '3'),('4', '4'),('5', '5')],
    )
    rating_datetime = serializers.DateTimeField(auto_now_add=True)

    class Meta:
        model = models.Ratings
        fields = '__all__'
        read_only_fields = ['patron']