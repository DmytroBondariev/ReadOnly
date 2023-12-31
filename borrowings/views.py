from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnBookSerializer
)
from borrowings.tasks import send_telegram_notification


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Borrowing.objects.select_related("book", "user")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "return_book":
            return BorrowingReturnBookSerializer
        return BorrowingListSerializer

    def perform_create(self, serializer):
        borrowing = serializer.save()

        message = (
            f"New borrowing created: "
            f"User {borrowing.user.email} borrowed book '{borrowing.book.title}'. "
            f"Expected return date: {borrowing.expected_return_date}."
        )
        send_telegram_notification.delay(message)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        if is_active is not None:
            if is_active.lower() == "true":
                """Filter for active borrowings (actual_return_date is None)"""
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                """Filter for inactive borrowings (actual_return_date is not None)"""
                queryset = queryset.filter(actual_return_date__isnull=False)
        if user.is_staff:
            if user_id:
                queryset = queryset.filter(user_id=user_id)
            return queryset
        return queryset.filter(user=user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=str,
                description="Filter borrowings by active/inactive status"
            ),
            OpenApiParameter(
                "user_id",
                type=int,
                description="Filter borrowings by user id: "
                            "available only for admin users",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        """Update borrowing with actual_return_date"""
        borrowing = self.get_object()

        if borrowing.user != request.user:
            return Response(
                "You are not allowed to return this book.",
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(
            borrowing,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Book returned successfully.")
