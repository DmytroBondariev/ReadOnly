from django.db import models
from rest_framework.exceptions import ValidationError


class Book(models.Model):
    COVER_CHOICES = (
        ("soft", "Soft"),
        ("hard", "Hard"),
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(default=0)

    def clean(self):
        if self.inventory < 0:
            raise ValidationError("Inventory cannot be less than 0.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.title} by {self.author}, "
            f"{self.cover} cover, {self.inventory} in stock, "
            f"${self.daily_fee} per day"
            )

    class Meta:
        ordering = ["title", "author", "cover"]
        unique_together = ["title", "author", "cover"]
