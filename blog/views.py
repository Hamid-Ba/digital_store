"""
Blog Module Views
"""
from django.utils import timezone
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from config import pagination
from blog import serializers, models


class BlogDetailView(generics.RetrieveAPIView):
    """Detail Of Blog View"""

    lookup_field = "slug"
    queryset = models.Blog.objects.all()
    serializer_class = serializers.BlogSerializer


class BlogsView(generics.ListAPIView):
    """List Of Blogs View"""

    queryset = models.Blog.objects.all()
    pagination_class = pagination.StandardPagination
    serializer_class = serializers.BlogSerializer

    def get_queryset(self):
        return self.queryset.filter(publish_date__lte=timezone.now()).order_by(
            "-publish_date"
        )


class LatestBlogsView(generics.ListAPIView):
    """List Of Latest Blogs View"""

    queryset = models.Blog.objects.order_by("-publish_date")
    serializer_class = serializers.LatestBlogSerializer

    def get_queryset(self):
        return self.queryset.filter(publish_date__lte=timezone.now())[:3]


class SearchBlogsAPI(generics.ListAPIView):
    """Search Blogs API"""

    queryset = models.Blog.objects.all()
    serializer_class = serializers.BlogSerializer
    pagination_class = pagination.StandardPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = ["publish_date"]
    search_fields = ["title", "slug", "short_desc", "category__title"]

    def get_queryset(self):
        return self.queryset.filter(publish_date__lte=timezone.now()).order_by(
            "-publish_date"
        )
