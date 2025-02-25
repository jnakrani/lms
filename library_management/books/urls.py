from django.urls import path
from .views import BookListView, BorrowBookView, ReturnBookView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('borrow/<int:book_id>/', BorrowBookView.as_view(), name='borrow-book'),
    path('return/<int:book_id>/', ReturnBookView.as_view(), name='return-book'),
]
