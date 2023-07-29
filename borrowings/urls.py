from django.urls import path

from borrowings.views import BorrowingViewSet

borrowing_list = BorrowingViewSet.as_view(actions={"get": "list", "post": "create"})
borrowing_detail = BorrowingViewSet.as_view(actions={"get": "retrieve"})

urlpatterns = [
    path("borrowings/", borrowing_list, name="borrowing-list"),
    path("borrowings/<int:pk>", borrowing_detail, name="borrowing-detail"),
]


app_name = "borrowings"
