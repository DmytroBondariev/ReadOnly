from django.urls import path
from rest_framework import routers

from borrowings.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)
# borrowing_list = BorrowingViewSet.as_view(actions={"get": "list", "post": "create"})
# borrowing_detail = BorrowingViewSet.as_view(actions={"get": "retrieve"})
# borrowing_return_book = BorrowingViewSet.as_view(actions={"patch": "return_book"})
urlpatterns = router.urls
# urlpatterns = [
#     path("borrowings/", borrowing_list, name="borrowing-list"),
#     path("borrowings/<int:pk>", borrowing_detail, name="borrowing-detail"),
#     path(
#         "borrowings/<int:pk>/return_book",
#         borrowing_return_book,
#         name="borrowing-return-book"
#     ),
# ]


app_name = "borrowings"
