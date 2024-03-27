from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("books/", views.BookListView.as_view(), name='books'),
    path("book/<int:pk>/", views.BookDetailView.as_view(), name='book-detail'),
    path("book/create/", views.BookCreate.as_view(), name='book-create'),
    path("book/<int:pk>/update/", views.BookUpdate.as_view(), name='book-update'),
    path("book/<int:pk>/delete/", views.BookDelete.as_view(), name='book-delete'),
    path("book/<int:pk>/instance/create/", views.BookInstanceCreate.as_view(), name='bookinstance-create'),
    path("book/<int:bookpk>/instance/<uuid:pk>/update/", views.BookInstanceUpdate.as_view(), name='bookinstance-update'),
    path("book/<int:bookpk>/instance/<uuid:pk>/delete/", views.BookInstanceDelete.as_view(), name='bookinstance-delete'),
    path("authors/", views.AuthorListView.as_view(), name='authors'),
    path("author/<int:pk>/", views.AuthorDetailView.as_view(), name='author-detail'),
    path("author/create/", views.AuthorCreate.as_view(), name='author-create'),
    path("author/<int:pk>/update/", views.AuthorUpdate.as_view(), name='author-update'),
    path("author/<int:pk>/delete/", views.AuthorDelete.as_view(), name='author-delete'),
    path('mybooks/', views.LoanedBooksUserListView.as_view(), name='my-books'),
    path('all-borrowed/', views.LoanedBookListAll.as_view(), name='all-borrowed'),
    path("books/<uuid:pk>/renew/", views.renew_book_librarian, name='renew-book-librarian'),
]
