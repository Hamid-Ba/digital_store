"""
site info modules views
"""

from rest_framework import generics, mixins, viewsets, views
from rest_framework.response import Response

from siteinfo import models, serializers
from config import pagination


class AboutUsView(generics.RetrieveAPIView):
    """About Us View"""

    serializer_class = serializers.AboutUsSerializer
    queryset = models.AboutUs.objects.all()

    def get(self, request):
        about_us = models.AboutUs.objects.first()
        serializer = serializers.AboutUsSerializer(about_us)
        return Response(serializer.data)


class ContactUsView(generics.ListAPIView):
    """Contact Us View"""

    queryset = models.ContactUs.objects.all()
    serializer_class = serializers.ContactUsSerializer


class HomeHeaderView(generics.RetrieveAPIView):
    """Contact Us View"""

    queryset = models.HomeHeader.objects.all()
    serializer_class = serializers.HomeHeaderSerializer

    def get(self, request):
        home_header = models.HomeHeader.objects.filter(is_active=True).first()
        serializer = serializers.HomeHeaderSerializer(home_header)
        return Response(serializer.data)


class FooterView(generics.RetrieveAPIView):
    """Contact Us View"""

    queryset = models.Footer.objects.all()
    serializer_class = serializers.FooterSerializer

    def get(self, request):
        footer = models.Footer.objects.filter(is_active=True).first()
        serializer = serializers.FooterSerializer(footer)
        return Response(serializer.data)


class SliderAndBannerView(generics.ListAPIView):
    """Contact Us View"""

    queryset = models.SliderAndBanner.objects.all()
    serializer_class = serializers.SliderAndBannerSerializer


class CreateTicketAPI(generics.CreateAPIView):
    """Create Ticket View"""

    queryset = models.Ticket.objects.all()
    serializer_class = serializers.TicketSerializer


class FAQCategoryViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = models.FAQCategory.objects.all()
    serializer_class = serializers.FAQCategorySerializer


class FAQViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = models.FAQ.objects.all()
    serializer_class = serializers.FAQSerializer
    pagination_class = pagination.StandardPagination


class EmailAndPhoneAPI(generics.RetrieveAPIView):
    queryset = models.EmailAndPhone.objects.all()
    serializer_class = serializers.EmailAndPhoneSerializer
