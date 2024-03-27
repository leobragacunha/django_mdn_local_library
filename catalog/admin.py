from django.contrib import admin
from .models import Author, Book, BookInstance, Genre, Language

# Register your models here.

class BookInline(admin.StackedInline):
    model = Book
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','date_of_birth','date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

admin.site.register(Author,AuthorAdmin)


# Inline class to display book instances on Book Section on Admin.
class BookInstanceInline(admin.TabularInline):
     model = BookInstance
     extra = 0

class BookAdmin(admin.ModelAdmin):
    # Check models.py to see more about display_genre in the Book Model.
    # (As Book and Genre has a Many-To-Many relationship, we can't assign them directly).
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

admin.site.register(Book, BookAdmin)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id', 'borrower')

    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, { 'fields': ('book', 'imprint','id') }),
        ('Availability', { 'fields': ('status','due_back', 'borrower') }),
    )



# admin.site.register(BookInstance, BookInstanceAdmin)


class GenreAdmin(admin.ModelAdmin):
    pass

admin.site.register(Genre, GenreAdmin)


class LanguageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Language, LanguageAdmin)