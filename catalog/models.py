from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

from datetime import date

import uuid # Creates an unique id for each book instance

# Create your models here.

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Text fields are used for bigger texts
    summary = models.TextField(max_length=1000, 
                               help_text="Enter a brief description of the book.")
    isbn = models.CharField("ISBN", max_length=13, 
                            help_text= "13 Character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>")
    genre = models.ManyToManyField(Genre,
                                   help_text="Select a genre for this book.")
    language = models.ForeignKey("Language", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    # Returns the url to access a detail record for this book
    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
    
    
    # Function to return a concatenate of genres for BookAdmin.
    # (As Book and Genre has a Many-To-Many relationship, we can't assign them directly).
    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"    

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                          help_text="Unique ID for this particular book, across the whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True,blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On Loan'),
        ('a','Available'),
        ('r','Reserved')
        )
    
    status = models.CharField(max_length=1, choices=LOAN_STATUS,blank=True,default='m',
                              help_text="Book availability")
    
    class Meta():
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)


    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.book.id})
        
    

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died',null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']

    # Returns the url to access a detail record for this book
    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Language(models.Model):
    language = models.CharField(max_length=50, unique=True,
                                help_text="Enter the book's natural language (e.g. English, French, etc.)")

    def __str__(self):
        return self.language