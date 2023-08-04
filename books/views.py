from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Book
from books.serializers import (
    BookCreateSerializer,
    BookListSerializer,
    BookDetailSerializer
)


class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    pagination_class = BookPagination
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "create":
            return BookCreateSerializer
        elif self.action == "retrieve":
            return BookDetailSerializer
        return BookListSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticatedOrReadOnly()]
        elif self.action == "retrieve":
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                description="Filter books by title"
            ),
            OpenApiParameter(
                name="author",
                type=str,
                description="Filter books by author"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
