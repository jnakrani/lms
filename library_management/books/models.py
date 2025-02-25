import re
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.
def validate_isbn(value):
    pattern = r'^\d{3}-\d{1}-\d{2}-\d{6}-\d{1}$'
    if not re.match(pattern, value):
        raise ValidationError("ISBN must be a formate is 000-0-00-000000-0.")


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=17, unique=True, validators=[validate_isbn])
    page_count = models.IntegerField()
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_loans")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_loans")
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"


