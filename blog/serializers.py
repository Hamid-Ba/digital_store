"""
Blog Module Serializer
"""
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer

from blog import models
from gallery import serializers as gallery_serializers


class BlogCategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""

    class Meta:
        model = models.BlogCategory
        fields = "__all__"


# class SpecificationSerializer(serializers.ModelSerializer):
#     """Specification Serializer"""

#     class Meta:
#         model = models.Specification
#         fields = "__all__"


class BlogSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Blog Serializer"""

    tags = TagListSerializerField()
    category = BlogCategorySerializer(many=False)
    # specs = SpecificationSerializer(many=True)
    image = gallery_serializers.GallerySerializer(many=False)

    class Meta:
        model = models.Blog
        fields = "__all__"


class LatestBlogSerializer(serializers.ModelSerializer):
    """Latest Blog Serializer"""

    category = BlogCategorySerializer(many=False)
    image = gallery_serializers.GallerySerializer(many=False)

    class Meta:
        model = models.Blog
        fields = ["title", "slug", "category", "image"]
