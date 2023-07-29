from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer, BorrowingDetailSerializer, BorrowingCreateSerializer


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
            return queryset
        return queryset.filter(user=user)
