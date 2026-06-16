from django.urls import path

from books import views

app_name = "books"
urlpatterns = [
    path("",views.main_page,name="home_page"),
    path("all-books/", views.BookListView.as_view(), name="all_books"),
    path("categories/", views.CategoryListAnn.as_view(), name="category"),
    path("categories/<slug:slug>/", views.BookByCategory.as_view(), name="books_by_category"),
    path("search/",views.SearchBooksView.as_view(),name="search_books"),
    path("suggestions/", views.BookSuggestionCreate.as_view(), name="suggestions"),
    path("detail-book/<int:pk>",views.BookView.as_view(),name="book_detail"),

    path("all-books/<int:pk>/delete",views.BookDeleteDet.as_view(),name = "book_confirm_delete"),

    path("all-books/<int:pk>/update",views.BookUpdateDet.as_view(),name = "book_update")




]