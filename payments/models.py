from django.db import models

from borrowings.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "PENDING"),
        ("PAID", "PAID"),
    ]
    TYPE_CHOICES = [
        ("PAYMENT", "PAYMENT"),
        ("FINE", "FINE"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return (f"Payment ID: {self.pk}, "
                f"Status: {self.status}, "
                f"Type: {self.type}, "
                f"Borrowing ID: {self.borrowing_id}"
                )

    class Meta:
        ordering = ["id"]
