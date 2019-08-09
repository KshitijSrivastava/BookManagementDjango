from django.urls import path, include
from books import views
urlpatterns = [
    path('', views.index),
    path('list', views.BookListView.as_view(), name = 'book_list'),
    path('book/delete/<str:book_id>', views.book_delete, name = 'book_delete'),
    path('increase_book/<str:book_id>', views.increase_book, name = 'increase_book'),
    path('decrease_book/<str:book_id>', views.decrease_book, name = 'decrease_book'),
    path('search', views.search, name = 'search'),
    path('book_add/<str:book_id>', views.add_book, name = 'book_add'),

]
