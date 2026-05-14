from django.urls import path

from books import views


urlpatterns = [
    path("",views.main_page,name="main_page"),
    path("all-books/", views.all_books, name="all_books"),
    path("categories/", views.category, name="category"),
    path("categories/<slug:slug>/", views.books_by_category, name="books_by_category"),

    path("search/",views.search_books,name="search_books"),
]