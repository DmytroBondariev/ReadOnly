from rest_framework import serializers

from borrowings.serializers import BorrowingDetailSerializer
from .models import Payment


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "status", "type", "borrowing", "session_url", "session_id", "money_to_pay")


class PaymentDetailSerializer(serializers.ModelSerializer):
    borrowing = BorrowingDetailSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ("id", "status", "type", "borrowing", "session_url", "session_id", "money_to_pay")
