from rest_framework import serializers
from . import models

class RestTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30)
    
    class Meta:
        model = models.RestTag
        fields = ['id', 'title']