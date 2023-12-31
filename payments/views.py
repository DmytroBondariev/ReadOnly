import stripe
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payments.models import Payment
from payments.serializers import PaymentListSerializer, PaymentDetailSerializer


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
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
        return PaymentListSerializer

    @action(
        methods=["GET"],
        detail=False,
        url_path="success",
        url_name="payment-success",
    )
    def success(self, request):
        """Endpoint for successful stripe payment session"""
        session_id = request.query_params.get("session_id")
        payment = Payment.objects.get(session_id=session_id)
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == "paid":
            serializer = PaymentListSerializer(
                payment,
                data={"status": "PAID"},
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path="cancel",
        url_name="payment-cancel",
    )
    def cancel(self, request):
        """Endpoint for canceled stripe payment session"""
        session_id = request.query_params.get("session_id")
        payment = Payment.objects.get(session_id=session_id)

        serializer = PaymentListSerializer(payment)
        data = serializer.data

        return Response(data=data, status=status.HTTP_200_OK)
