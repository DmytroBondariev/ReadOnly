from rest_framework import serializers

from books.serializers import BookDetailBorrowingSerializer
from borrowing.models import Borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(slug_field="title", read_only=True)
    author = serializers.SlugRelatedField(slug_field="author", read_only=True)

    class Meta:
        model = Borrowing
        fields = ("is_active", "book", "author", "borrow_date", "expected_return_date",)


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookDetailBorrowingSerializer(read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "is_active",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )
