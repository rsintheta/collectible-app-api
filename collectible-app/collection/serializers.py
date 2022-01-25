from rest_framework import serializers
from base.models import Tag, Item, Collection


# Serializes a Tag
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


# Serializes an Item
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name')
        read_only_fields = ('id',)


# Serializes a Collection
class CollectionSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Item.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Collection
        fields = ('id', 'title', 'items', 'tags', 'items_in_collection',
                  'floor_price', 'link')
        read_only_fields = ('id',)


# Serializes a Collections details
class CollectionDetailSerializer(CollectionSerializer):
        items = ItemSerializer(many=True, read_only=True)
        tags = TagSerializer(many=True, read_only=True)


# Serializes uploaded images to Collections
class CollectionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'image')
        read_only_fields = ('id',)
