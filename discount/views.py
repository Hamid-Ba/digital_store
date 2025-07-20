from rest_framework import generics, response, status, permissions, authentication

from discount import serializers, models
from discount.services import discount_services

discount_service = discount_services.DiscountServices()


class DiscountCodeApiView(generics.RetrieveAPIView):
    queryset = models.DiscountCode.objects.all()
    serializer_class = serializers.DiscountSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def retrieve(self, request, code, *args, **kwargs):
        if discount_service.is_discount_code_valid(code, self.request.user):
            code = discount_service.get_discount_by(code)
            serializer = self.serializer_class(instance=code)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        return response.Response(
            {"message": "کد وارد شده معتبر نمی باشد"}, status=status.HTTP_403_FORBIDDEN
        )
