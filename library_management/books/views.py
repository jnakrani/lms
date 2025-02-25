from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from django.utils import timezone

from .models import Book, Loan
from .serializers import BookSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
# Book List with Filtering & Pagination
class BookListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = BookSerializer
    filterset_fields = ['title', 'author', 'availability']
    queryset = Book.objects.all()
    
    @swagger_auto_schema(
        operation_description="Retrieve a list of books with optional filters (title, author, availability).",
        tags=["Books"],
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="Filter books by title", type=openapi.TYPE_STRING),
            openapi.Parameter('author', openapi.IN_QUERY, description="Filter books by author", type=openapi.TYPE_STRING),
            openapi.Parameter('availability', openapi.IN_QUERY, description="Filter books by availability (True/False)", type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: BookSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# Borrow Book
class BorrowBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        book = Book.objects.filter(id=book_id, availability=True).first()
        
        if not book:
            return Response({"error": "Book not Available."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not book.availability:
            return Response({"error": "Book not available."}, status=status.HTTP_400_BAD_REQUEST)

        book.availability = False
        book.save()
        loan = Loan.objects.create(user=request.user, book=book)
        return Response({"message": "Book borrowed successfully."}, status=status.HTTP_201_CREATED)


# Return Book
class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        loan = Loan.objects.filter(user=request.user, book_id=book_id, returned_at=None).first()
        
        if not loan:
            return Response({"error": "This Book not borrowed by you."}, status=status.HTTP_400_BAD_REQUEST) or Response({"error": "Book not exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        loan.returned_at = timezone.now()
        loan.book.availability = True
        loan.book.save()
        loan.save()
        return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)
