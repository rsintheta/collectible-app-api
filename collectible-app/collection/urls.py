from django.urls import path, include
from rest_framework.routers import DefaultRouter

from collection import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'collection'

urlpatterns = [
    path('', include(router.urls))
]
