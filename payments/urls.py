from django.urls import path

from payments.views import PaymentViewSet

payment_list = PaymentViewSet.as_view(actions={"get": "list"})
payment_detail = PaymentViewSet.as_view(actions={"get": "retrieve"})
payment_success = PaymentViewSet.as_view(actions={"get": "success"})

urlpatterns = [
    path("payments/", payment_list, name="payment-list"),
    path("payments/<int:pk>", payment_detail, name="payment-detail"),
    path("payments/success/", payment_success, name="payment-success"),
]


app_name = "payment"
