from django.conf.urls import url, include
from rest_framework import routers
from .views import GoogleTokenToDjangoTokenViewSet

router = routers.DefaultRouter()
router.register(r'getUserToken', GoogleTokenToDjangoTokenViewSet, base_name='getUserToken')

urlpatterns = [
    url(r'^', include(router.urls)),
]

