from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from base.models import Tag, Item, Collection
from collection import serializers


# A basic viewset for Collection attributes
class BaseCollectionAttrViewset(viewsets.GenericViewSet,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Returns objects for the currently authenticated User only
    def get_queryset(self):
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(collection__isnull=False)
        return queryset.filter(
            user=self.request.user
            ).order_by('-name').distinct()

    # Creates a new object
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

    # Converts a list of string IDs to a list of integers
    def _params_to_ints(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    # Retrieves the Collection list for the authenticated User
    def get_queryset(self):
        tags = self.request.query_params.get('tags')
        items = self.request.query_params.get('items')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if items:
            item_ids = self._params_to_ints(items)
            queryset = queryset.filter(items__id__in=item_ids)
        return queryset.filter(user=self.request.user)

    # Returns the appropriate serializer class
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CollectionDetailSerializer
        elif self.action == 'upload_image':
            return serializers.CollectionImageSerializer
        return self.serializer_class

    # Creates a new Collection
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    # Uploads an image to a Collection
    def upload_image(self, request, pk=None):
        collection = self.get_object()
        serializer = self.get_serializer(
            collection,
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
