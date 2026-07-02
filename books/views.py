from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

import books
from books.models import Book, Category, BookSuggestion
from .forms import SearchForm, BookSuggestionForm, BookFormDet
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Book
from .forms import BookFormDet
from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count
from asgiref.sync import sync_to_async
# Create your views here.
def main_page(request):
    return render(request, "home_page.html")

class BookListView(ListView):
    model = Book
    template_name = "all_books.html"
    context_object_name = "books"
    paginate_by = 3
    page_kwarg = "page"


class BookView(DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"

class CategoryListAnn(ListView):
    model = Category
    template_name = "category.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.annotate(num_books=Count("books"))



class BookByCategory(ListView):
    model = Book
    template_name = "books_by_category.html"
    context_object_name = "result"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        category = Category.objects.get(slug=slug)
        return Book.objects.filter(category=category)

    def get_context_data(self,*args,**kwargs):
        slug = self.kwargs.get("slug")
        category = Category.objects.get(slug=slug)
        context = super().get_context_data(*args,**kwargs)
        context["category"] = category
        return context


class SearchBooksView(ListView):
    model = Book
    template_name = "search.html"
    context_object_name = "books"

    def get_queryset(self):
        search_form = SearchForm(self.request.GET)
        if search_form.is_valid():
            search_query = search_form.cleaned_data["query"]
            if search_query:
                return Book.objects.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query))
        return Book.objects.none()

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        search_form = SearchForm(self.request.GET)
        context["search_form"] = search_form
        return context


class BookSuggestionCreate(LoginRequiredMixin,CreateView):
    model = BookSuggestion
    form_class = BookSuggestionForm
    template_name = "suggestions.html"
    context_object_name = "form"
    success_url = reverse_lazy("home_page")

class BookUpdateDet(PermissionRequiredMixin,UpdateView):
    model = Book
    template_name = "book_update.html"
    form_class = BookFormDet
    success_url = reverse_lazy("home_page")
    permission_required = "books.change_book"


class BookDeleteDet(PermissionRequiredMixin,DeleteView):
    model = Book
    template_name = "book_confirm_delete.html"
    context_object_name = "book"
    success_url = reverse_lazy("home_page")
    permission_required = "books.delete_book"


async def all_books(request):
    books = [book async for book in Book.objects.all()]
    paginator = Paginator(books, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return await sync_to_async(render)(request, template_name="all_books.html",context={"books":page_obj.object_list, "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),})

async def category(request):
    categories = [category async for category in Category.objects.annotate(num_books=Count("books"))]
    return await sync_to_async(render)(request, template_name="category.html",context={"categories":categories})



async def books_by_category(request,slug):
  category = await sync_to_async(get_object_or_404)(Category, slug=slug)
  result =[ book async for book in Book.objects.filter(category=category)]
  context = {
      "category": category,
      "result": result
  }
  return await sync_to_async(render)(request, template_name="books_by_category.html",context=context)







# def all_books(request):
#     books = Book.objects.all()
#     return render(request,template_name="all_books.html",context={"books":books})



# def category(request):
#     categories = Category.objects.annotate(num_books=Count("book"))
#
#     return render(request,template_name="category.html",context={"categories":categories})


# def books_by_category(request, slug):
#     category = Category.objects.get(slug=slug)
#     result = Book.objects.filter(category=category)
#     return render(request, "books_by_category.html", {
#         "category": category,
#         "result": result,
#     })

# def search_books(request):
#    search_form = SearchForm(request.GET)
#    books = []
#    if search_form.is_valid():
#        search_query = search_form.cleaned_data["query"]
#        if search_query:
#            books = Book.objects.filter(
#                Q(title__icontains=search_query) |
#                Q(author__icontains=search_query)
#            )
#    return render(request, template_name="search.html", context={"books": books, "search_form":search_form})
#

# def get_queryset(self):
#     queryset = super().get_queryset()
#
#     query = self.request.GET.get("query")
#
#     if query:
#         queryset = queryset.filter(
#             Q(title__icontains=query) |
#             Q(author__icontains=query)
#         )
#
#     return queryset



# def suggestions(request):
#     if request.method == "POST":
#         form = BookSuggestionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, template_name="suggestions.html", context={"form":BookSuggestionForm(),"success":True})
#     else:
#         form = BookSuggestionForm()
#     return render(request, template_name="suggestions.html", context={"form":form})



# def book_update(request,pk):
#    book = get_object_or_404(Book,pk = pk)
#    if request.method == "POST":
#        form = BookFormDet(request.POST,instance=book)
#        if form.is_valid():
#            form.save()
#            return redirect("home_page")
#    else:
#        form = BookFormDet(instance=book)
#    return render(request,template_name="book_update.html",context={"form":form,"book":book})

# def book_delete(request,pk):
#     book = get_object_or_404(Book,pk = pk)
#     if request.method =="POST":
#         book.delete()
#         return redirect("books:home_page")
#     else:
#         return render(request, "book_confirm_delete.html", {
#             "book": book,
#         })





































