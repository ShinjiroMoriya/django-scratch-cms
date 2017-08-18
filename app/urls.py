from django.conf.urls import url
from .views import *
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'api/post', PostAPIView)

urlpatterns = [
    url(r'^login$', Login.as_view()),
]
