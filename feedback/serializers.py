from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
import restaurants.serializers as rs
import patron.models as pm
import restaurants.models as rm


User = get_user_model()


# Serializer for combined Review model
class ReviewsGetSerializer(serializers.ModelSerializer):
    
    menu_item = rs.MenuItemListSerializer()
    # menu_item = serializers.PrimaryKeyRelatedField(queryset=rm.MenuItem.objects.all())
    
    review = serializers.CharField(max_length=255)
    #rating = serializers.ChoiceField(
        #choices = [('1', '1'), ('2', '2'), ('3', '3'),('4', '4'),('5', '5')],
    #)
    rating = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        default=0.0
    )

    class Meta:
        model = models.Reviews
        fields = '__all__'
        read_only_fields = ['patron']

class ReviewsSerializer(serializers.ModelSerializer):
    
    # menu_item = rs.MenuItemListSerializer()
    menu_item = serializers.PrimaryKeyRelatedField(queryset=rm.MenuItem.objects.all())
    
    review = serializers.CharField(max_length=255)
    #rating = serializers.ChoiceField(
        #choices = [('1', '1'), ('2', '2'), ('3', '3'),('4', '4'),('5', '5')],
    #)
    rating = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        default=0.0
    )

    class Meta:
        model = models.Reviews
        fields = '__all__'
        read_only_fields = ['patron']

# Does App Satisfaction even need a get serializer, nothing is taken from another model's serializers
class AppSatisfactionGetSerializer(serializers.ModelSerializer):
    review = serializers.CharField(max_length=255)

    rating = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        default=0.0
    )

    class Meta:
        model = models.Reviews
        fields = '__all__'
        read_only_fields = ['user']

class AppSatisfactionSerializer(serializers.ModelSerializer):
    review = serializers.CharField(max_length=255)

    rating = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        default=0.0
    )

    class Meta:
        model = models.Reviews
        fields = '__all__'
        read_only_fields = ['user']


# Serializer for Reviews model
# class ReviewsSerializer(serializers.ModelSerializer):
#     # Uncommenting Patron may work
#     #patron = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
#     patron_review = serializers.CharField(max_length=255,null=True)
#     review_datetime = serializers.DateTimeField(auto_now_add=True)

#     class Meta:
#         model = models.Reviews
#         fields = '__all__'
#         read_only_fields = ['patron']

#     # def formatted_datetime(self):
#     #     return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')

# #Serializer for Ratings model    
# class RatingsSerializer(serializers.ModelSerializer):
#     #patron = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
#     ratings = serializers.IntegerField(
#         choices = [('1', '1'), ('2', '2'), ('3', '3'),('4', '4'),('5', '5')],
#     )
#     rating_datetime = serializers.DateTimeField(auto_now_add=True)

#     class Meta:
#         model = models.Ratings
#         fields = '__all__'
#         read_only_fields = ['patron']
