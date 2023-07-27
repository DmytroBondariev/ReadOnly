from django.db import models


class Book(models.Model):
    COVER_CHOICES = (
        ("soft", "Soft"),
        ("hard", "Hard"),
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField(default=0)
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        existing_book = Book.objects.filter(title=self.title, author=self.author, cover=self.cover).first()

        if existing_book:
            self.inventory = existing_book.inventory + 1
        else:
            self.inventory = 0

        super().save(*args, **kwargs)
