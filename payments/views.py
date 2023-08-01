from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from payments.models import Payment
from payments.serializers import PaymentListSerializer, PaymentDetailSerializer


class PaymentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Payment.objects.select_related("borrowing")
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if user.is_staff:
            return queryset
        return queryset.filter(borrowing__user=user)

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        if self.action == "retrieve":
            return PaymentDetailSerializer
