from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from base.models import Tag, Item, Collection
from collection import serializers


# Base viewset for user owned collection attributes
class BaseCollectionAttrViewset(viewsets.GenericViewSet,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Return objects for the currently authenticated user only
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # Create a new user object
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Manages Tags in the database
class TagViewSet(BaseCollectionAttrViewset):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


# Manages Items in the database
class ItemViewSet(BaseCollectionAttrViewset):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer


# Manages Collections in the database
class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CollectionSerializer
    queryset = Collection.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Retrieves the Collection list for the authenticated user
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    # Returns the appropriate serializer class
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CollectionDetailSerializer
        return self.serializer_class

    # Creates a new collection
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
