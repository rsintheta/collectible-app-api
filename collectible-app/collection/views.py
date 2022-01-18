from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from base.models import Tag, Item
from collection import serializers


# Manages tags in the database
class TagViewSet(viewsets.GenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # Returns objects from database that belong to the authenticated user only
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # Create a new user tag
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Manages Items in the database
class ItemViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer

    # Returns objects for the current authenticated user
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')
