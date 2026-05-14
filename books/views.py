from django.db.models import Count
from django.shortcuts import render


from books.models import Book, Category
from .forms import SearchForm
from django.db.models import Q

# Create your views here.
def main_page(request):
    return render(request, "main_page.html")


def all_books(request):
    books = Book.objects.all()
    return render(request,template_name="all_books.html",context={"books":books})


def category(request):
    categories = Category.objects.annotate(num_books=Count("book"))

    return render(request,template_name="category.html",context={"categories":categories})


def books_by_category(request, slug):
    category = Category.objects.get(slug=slug)
    result = Book.objects.filter(category=category)
    return render(request, "books_by_category.html", {
        "category": category,
        "result": result,
    })

def search_books(request):
   search_form = SearchForm(request.GET)
   books = []
   if search_form.is_valid():
       search_query = search_form.cleaned_data["query"]
       if search_query:
           books = Book.objects.filter(
               Q(title__icontains=search_query) |
               Q(author__icontains=search_query)
           )
   return render(request, template_name="search.html", context={"books": books, "search_form":search_form})




















