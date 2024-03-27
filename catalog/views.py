from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from .models import Author, Book, BookInstance, Genre, Language
from .forms import RenewBook, RenewBookModelForm
# Create your views here.


def index(request):
    
    # Variables for counting objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books 
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()

    # OBS: when we don't specify any filter, the .all() method is implied
    num_authors = Author.objects.count() # Same as Author.objects.all().count()

    # Challenge
    num_genres = Genre.objects.count()
    num_hp_instances = BookInstance.objects.filter(book__title__contains = "Harry Potter").count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genres':num_genres,
        'num_hp_instances':num_hp_instances,
        'num_visits':num_visits,
    }

    return render(request, 'catalog/index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 5 # Usually we paginate by more records, but this is just a pagination example!

    # Standard return: model_name_lowercased_list.html
    template_name = "catalog/book_list.html"

    # Function that returns the query the view will use
    # def get_queryset(self):
    #     return Book.objects.filter(title__contains = "Harry Potter") [:5]
    
    # Function that returns the context object from this view
    def get_context_data(self, **kwargs: Any):
        context = super(BookListView,self).get_context_data(**kwargs)
        
        # We can add data on this context object
        # context['new object'] = "A new object"
        
        return context
    
    
class BookDetailView(generic.DetailView):
    model = Book


    # template_name = 'book_detail.html'    # Standard
    # context_object_name = 'book'          # Standard


class AuthorListView(generic.ListView):
    model = Author
    paginate_by=5


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksUserListView(LoginRequiredMixin, generic.ListView):
    model=BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact = 'o').order_by('due_back')
    

class LoanedBookListAll(PermissionRequiredMixin, generic.ListView):
    model=BookInstance
    permission_required=('catalog.can_mark_returned',)
    template_name='catalog/bookinstance_list_borrowed_all.html'
    paginate_by=2

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact = 'o').order_by('due_back')
    

def renew_book_librarian(request, pk):
    # Before doing anything we need to grab the book instance we are manipulating
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        # Using form
        # form = RenewBook(request.POST)
        # Using modelForm
        form = RenewBookModelForm(request.POST)


        if form.is_valid():
            # Setting BookInstance.due_back according to the entered date in form
            # book_instance.due_back = form.cleaned_data['renewal_date']    # form
            book_instance.due_back = form.cleaned_data['due_back']        # modelForm
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    # In case there is no post yet
    else:

        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # form = RenewBook(initial={'renewal_date':proposed_renewal_date})  # form
        form = RenewBookModelForm(initial={'due_back':proposed_renewal_date})  # modelForm

    context = {
        'form':form,
        'book_instance':book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(generic.CreateView):
    model=Author
    fields="__all__"    # Mandatory on CreateView
    initial={'date_of_birth':datetime.date.today()}
    # template_name = 'modelname_form.html'   # Standard


class AuthorUpdate(generic.UpdateView):
    model=Author
    fields=['first_name','last_name','date_of_birth','date_of_death']
    # template_name = 'modelname_form.html'   # Standard


class AuthorDelete(generic.DeleteView):
    model=Author
    success_url=reverse_lazy('authors')
    # Needs a model_name_confirm_delete.html template


class BookCreate(generic.CreateView):
    model=Book
    fields="__all__"

class BookUpdate(generic.UpdateView):
    model=Book
    fields="__all__"
    
class BookDelete(generic.DeleteView):
    model=Book 
    success_url = reverse_lazy('books')


class BookInstanceCreate(generic.CreateView):
    model = BookInstance
    fields = ['imprint', 'status', 'due_back']
    
    # This function only gets the Book Object, for displaying the title in the view 
    def get_context_data(self, **kwargs):
        context = super(BookInstanceCreate,self).get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs['pk'])
        # context['book'] = self.get_object()
        return context
    
    # This function gets the book as a pk and add it to the form itself
    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        form.instance.book = book
        return super(BookInstanceCreate,self).form_valid(form)
    

class BookInstanceUpdate(generic.UpdateView):

    model=BookInstance
    fields=['imprint','status', 'due_back','borrower']
    template_name = 'catalog/bookinstance_edit_form.html'

    def get_context_data(self, **kwargs):
        context = super(BookInstanceUpdate,self).get_context_data(**kwargs)
        # We only need the PK in the get method. The url link will be generated with 
        # the reverse function and the urlpattern set.
        # context['bookinstance'] = get_object_or_404(BookInstance, pk=self.kwargs['pk'])
        context['bookinstance'] = self.get_object()
        return context


class BookInstanceDelete(generic.DeleteView):
    model=BookInstance

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(*args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={"pk": self.object.book.id})