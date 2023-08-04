import os

import stripe
from rest_framework.request import Request
from rest_framework.reverse import reverse

from borrowings.models import Borrowing
from payments.models import Payment

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
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


def create_stripe_session(
    borrowing,
    request,
    payment_type,
    overdue_days,
):
    book = borrowing.book
    if overdue_days is None:
        days_borrowed = (
            borrowing.expected_return_date - borrowing.borrow_date
        ).days
        fee = int(book.daily_fee * days_borrowed * 100)
        title = f"Payment for borrowing of {book.title}"
    else:
        fee = int(book.daily_fee * overdue_days * 100) * FINE_MULTIPLIER
        title = (
            f"Fine payment for {book.title}: {overdue_days} days overdue"
        )
    success_url = reverse("payment:payment-success", request=request)
    cancel_url = reverse("payment:payment-cancel", request=request)

    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": title,
                    },
                    "unit_amount": fee,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url + "?session_id={CHECKOUT_SESSION_ID}",
    )
    create_payment(borrowing, session, payment_type)
    return session
