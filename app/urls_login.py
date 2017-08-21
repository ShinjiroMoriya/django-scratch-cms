from django.conf.urls import url
from .views import *
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'api/image', PostImageAPIView)
router.register(r'api/pdf', PostPdfAPIView)
router.register(r'api/post', PostAPIView)

urlpatterns = [
    url(r'^$', PostTop.as_view()),
    url(r'^post_(?P<post_id>[\w\-]+)$', PostDetail.as_view()),
    url(r'^post$', PostIndex.as_view()),
    url(r'^post/page/(?P<page>[0-9]+)$', PostIndex.as_view()),
    url(r'^post/create$', PostCreate.as_view()),
    url(r'^post/edit/(?P<post_id>[\w\-]+)$', PostEdit.as_view()),
    url(r'^post/delete/(?P<post_id>[\w\-]+)$', PostDelete.as_view()),
    url(r'^post/preview/(?P<post_id>[\w\-]+)$', PostPreview.as_view()),
    url(r'^post/status/(?P<post_id>[\w\-]+)$', PostStatus.as_view()),
    url(r'^post/image$', PostImageIndex.as_view()),
    url(r'^post/image/page/(?P<page>[0-9]+)$', PostImageIndex.as_view()),
    url(r'^post/image/delete/(?P<image_id>[\w\-]+)$', PostImageDelete.as_view()),
    url(r'^image/add$', PostImageAdd.as_view()),
    url(r'^post/pdf$', PostPdfIndex.as_view()),
    url(r'^post/pdf/page/(?P<page>[0-9]+)$', PostPdfIndex.as_view()),
    url(r'^post/pdf/delete/(?P<pdf_id>[\w\-]+)$', PostPdfDelete.as_view()),
    url(r'^pdf/add$', PostPdfAdd.as_view()),
    url(r'^logout$', Logout.as_view()),
]
