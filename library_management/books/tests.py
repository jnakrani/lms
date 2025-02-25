from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Book, Loan
from .serializers import BookSerializer

# Create your tests here.
class BookTestCase(APITestCase):
    
    def setUp(self):
        self.book = Book.objects.create(title="Test Book", author="Author", isbn="000-0-00-000001-1", page_count=200, availability=False)
        self.book1 = Book.objects.create(title="Django for Beginners", author="William S. Vincent", isbn="000-0-00-000001-2", page_count=20, availability=True)
        self.book2 = Book.objects.create(title="Python Crash Course", author="Eric Matthes", isbn="000-0-00-000001-3", page_count=25, availability=True)
        self.book3 = Book.objects.create(title="Django REST Framework Guide", author="Tom Christie", isbn="000-0-00-000001-4", page_count=55, availability=True)
        
        self.url = reverse('book-list')
        
    def test_get_book_list(self):
        self.client = APITestCase()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = Book.objects.all()
        expected_data = BookSerializer(books, many=True).data
        self.assertEqual(response.data['results'], expected_data)

    def test_filter_books_by_title(self):
        response = self.client.get(self.url, {'title': 'Django for Beginners'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Django for Beginners")

    def test_filter_books_by_author(self):
        response = self.client.get(self.url, {'author': 'Tom Christie'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['author'], "Tom Christie")

    def test_filter_books_by_availability(self):
        response = self.client.get(self.url, {'availability': 'false'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) 
        
        
class LoanListViewTestCase(APITestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password123")

        refresh = RefreshToken.for_user(self.user1)
        self.token1 = str(refresh.access_token)
        
        self.book1 = Book.objects.create(title="Django for Beginners", author="William S. Vincent", isbn="000-0-00-000001-2", page_count=20, availability=True)
        self.borrow_url = reverse('borrow-book', kwargs={'book_id': self.book1.id})


    def test_book_borrow(self):
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')

        first_response = self.client.post(self.borrow_url)
        
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(first_response.data['message'], "Book borrowed successfully.")
        self.assertTrue(Loan.objects.filter(user=self.user1, book=self.book1, returned_at=None).exists())
        
        second_response = self.client.post(self.borrow_url)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(second_response.data['error'], "Book not Available.")        
        