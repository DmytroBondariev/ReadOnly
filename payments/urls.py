from django.urls import path

from payments.views import PaymentViewSet

payment_list = PaymentViewSet.as_view(actions={"get": "list"})
payment_detail = PaymentViewSet.as_view(actions={"get": "retrieve"})
payment_success = PaymentViewSet.as_view(actions={"get": "success"})
payment_cancel = PaymentViewSet.as_view(actions={"get": "cancel"})

urlpatterns = [
    path("payments/", payment_list, name="payment-list"),
    path("payments/<int:pk>", payment_detail, name="payment-detail"),
    path("payments/success/", payment_success, name="payment-success"),
    path("payments/cancel/", payment_cancel, name="payment-cancel"),
]


app_name = "payment"
