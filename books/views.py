from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, CreateView, ListView, UpdateView

from books.models import Book
from books.forms import BookForm
import requests


def index(request):
    return render(request, 'books/index.html')
    return HttpResponse('Index')

class BookListView(ListView):
    """
    Return the list of Books
    """
    template_name = 'books/books_list.html'
    model = Book


def book_delete(request, book_id):
    """
    Function for deleting a book in the inventory
    """
    book = get_object_or_404(Book, book_id=book_id)
    #print('Book is deleted')
    book.delete()
    return redirect('book_list')


def increase_book(request, book_id):
    """
    Function for increasing the books in inventory
    """
    book = get_object_or_404(Book, book_id=book_id)
    book.copies += 1
    book.save()
    return redirect('book_list')


def decrease_book(request, book_id):
    """
    Function for decreasing the books in the inventory
    """
    book = get_object_or_404(Book, book_id=book_id)
    if book.copies == 0:
        return redirect('book_list')
    elif book.copies == 1:
        return redirect('book_delete', book_id = book_id)
    else:
        book.copies -= 1
        book.save()
        return redirect('book_list')


def add_book(request, book_id):
    """
    For adding a new book in the Inventory by searching in Google Books
    """
    try:
        book = Book.objects.get(book_id = book_id)
        increase_book(request, book_id)
        # return redirect('book_list')
    except:
        key = 'AIzaSyDwXeYjarTARFI9bfX8bs96rqt0R3VZkwk'
        url = "https://www.googleapis.com/books/v1/volumes/{}?key={}".format(book_id, key)
        response = requests.get(url)
        data = response.json()
        print(data)
        book_name = data['volumeInfo']['title']
        authors = data['volumeInfo']['authors']
        if authors is not None:
            authors = ", ".join(authors)
        new_book = Book(book_name = book_name, author = authors , book_id = book_id, copies = 1 )
        new_book.save()

    return redirect('book_list')



def search(request):
    """
    To search in the Google Books API for the query term
    """
    context = {}
    q = request.GET.get('query', None)
    google_id = 'AIzaSyDwXeYjarTARFI9bfX8bs96rqt0R3VZkwk'
    if q is not None:
        response = requests.get('https://www.googleapis.com/books/v1/volumes?q={}&id={}'.format(q, google_id))
        data = response.json()
        book_lst = []
        for item in data['items']:
            book_item = {}
            id = item.get('id', None)

            try:
                book = Book.objects.get(book_id = id)
                is_available = True
            except:
                is_available = False

            title = item['volumeInfo'].get('title', None)
            authors  = item['volumeInfo'].get('authors', None)

            if authors is not None:
                authors = ', '.join(authors)
            book_item['id'] = id
            book_item['is_available'] = is_available
            book_item['title'] = title
            book_item['authors'] = authors

            book_lst.append(book_item)

    context['book_list'] = book_lst
    return render(request, 'books/book_search.html', context)