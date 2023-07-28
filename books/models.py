from django.db import models


class Book(models.Model):
    COVER_CHOICES = (
        ("soft", "Soft"),
        ("hard", "Hard"),
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

    @property
    def inventory(self):
        return Book.objects.filter(title=self.title, author=self.author, cover=self.cover).count()
