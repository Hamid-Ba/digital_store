from rest_framework import viewsets, permissions, authentication

from address import models, serializers


# Create your views here.
class AddressViewSet(viewsets.ModelViewSet):
    """Address View Set"""

    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
