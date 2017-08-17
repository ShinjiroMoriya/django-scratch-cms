from rest_framework import serializers
from app.models import Post, PostImage, PostPdf
from django.conf import settings


class PostSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField('get_url')

    class Meta:
        model = Post
        fields = (
            'post_id',
            'title',
            'contents',
            'status',
            'publish_date',
            'registration_date',
            'detail',
        )

    @staticmethod
    def get_url(obj):
        return settings.URL + '/api/post/' + obj.post_id


class PostRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'post_id',
            'title',
        )


class PostImageSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = PostImage
        fields = (
            'image_id',
            'title',
            'value',
        )

    @staticmethod
    def get_image_url(obj):
        return obj.image_url


class PostPdfSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_pdf_url')

    class Meta:
        model = PostPdf
        fields = (
            'pdf_id',
            'title',
            'value',
        )

    @staticmethod
    def get_pdf_url(obj):
        return obj.pdf_url
