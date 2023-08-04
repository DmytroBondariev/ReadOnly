from django.urls import path

from payments.views import PaymentViewSet

payment_list = PaymentViewSet.as_view(actions={"get": "list"})
payment_detail = PaymentViewSet.as_view(actions={"get": "retrieve"})
urlpatterns = [
    path("payments/", payment_list, name="payment-list"),
    path("payments/<int:pk>", payment_detail, name="payment-detail"),
]


app_name = "payment"
