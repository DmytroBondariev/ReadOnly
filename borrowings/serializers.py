from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.serializers import BookDetailBorrowingSerializer
from borrowings.models import Borrowing
from payments.models import Payment


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(slug_field="title", read_only=True)
    author = serializers.SlugRelatedField(slug_field="author", read_only=True)

    class Meta:
        model = Borrowing
        fields = ("id", "is_active", "book", "author", "borrow_date", "expected_return_date", "actual_return_date",)


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookDetailBorrowingSerializer(read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "is_active",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("book", "expected_return_date",)

    def validate(self, data):
        """Check if the book inventory is not 0"""
        book = data["book"]
        user = self.context["request"].user
        if book.inventory == 0:
            raise serializers.ValidationError("Book is not available for borrowing.")

        """Check if the expected_return_date is not in the past"""
        expected_return_date = data["expected_return_date"]
        if expected_return_date <= date.today():
            raise serializers.ValidationError("Expected return date must be in the future.")

        pending_payments = Payment.objects.filter(borrowing__user=user).filter(
            status="PENDING"
        )

        if pending_payments:
            raise ValidationError(
                detail="You have one or more pending payments. "
                       "You can't make borrowings until you pay for them."
            )
        return data

    def create(self, validated_data):
        """Decrease book inventory by 1"""
        book = validated_data["book"]
        book.inventory -= 1
        book.save()

        """Attach the current user to the borrowing"""
        user = self.context["request"].user
        borrowing = Borrowing.objects.create(user=user, **validated_data)
        return borrowing


class BorrowingReturnBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ()

    def update(self, instance, validated_data):
        """Validate if the borrowing has already been returned"""
        if self.instance.actual_return_date:
            raise serializers.ValidationError("Borrowing has already been returned.")

        instance.actual_return_date = date.today()

        """Increase book inventory by 1"""
        book = instance.book
        book.inventory += 1

        book.save()
        instance.save()

        return instance
