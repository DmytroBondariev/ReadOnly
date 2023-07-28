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
        same_books_with_same_cover = Book.objects.filter(title=self.title, author=self.author, cover=self.cover)
        existing_book = same_books_with_same_cover.first()

        if same_books_with_same_cover:
            self.inventory = existing_book.inventory + 1
            for book in same_books_with_same_cover:
                book.inventory += 1
                book.save()
        else:
            self.inventory = 1

        super().save(*args, **kwargs)
