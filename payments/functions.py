import os

import stripe
from rest_framework.request import Request
from rest_framework.reverse import reverse

from borrowings.models import Borrowing
from payments.models import Payment

stripe.secret_key = os.getenv("STRIPE_SECRET_KEY")
FINE_MULTIPLIER = 2


def create_payment(
        borrowing,
        session,
        payment_type
):
    Payment.objects.create(
        status="Pending",
        type=payment_type,
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=session.amount_total / 100,
    )
