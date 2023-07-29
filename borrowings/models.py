from django.db import models

from books.models import Book
from user.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def is_active(self):
        return self.actual_return_date is None

    def __str__(self):
        return f"User(id: {self.user.id}) borrowed book({self.book.title}, id: {self.book.id})"

    class Meta:
        ordering = ["-borrow_date"]
