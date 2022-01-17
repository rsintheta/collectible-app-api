from rest_framework import serializers
from base.models import Tag


# Serializer for tag objects
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
