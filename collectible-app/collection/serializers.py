from rest_framework import serializers
from base.models import Tag, Item


# Serializer for tag objects
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


# Serializer for items
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name')
        read_only_fields = ('id',)
