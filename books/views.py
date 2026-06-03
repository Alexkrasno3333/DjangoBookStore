from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from books.models import Book, Category, BookSuggestion
from .forms import SearchForm, BookSuggestionForm, BookFormDet
from django.db.models import Q
from django.urls import reverse_lazy
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
        return Category.objects.annotate(num_books=Count("book"))



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


































