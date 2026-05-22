from django.contrib import admin
from .models import Category,Book,BookSuggestion

class BookInline(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =['name','slug']
    search_fields = ['name']
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "price", "stock", "category"]
    search_fields = ["title", "author"]
    list_filter = ["category", "author"]


@admin.register(BookSuggestion)
class BookSuggestionAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "book_title", "author", "created_at"]
    search_fields = ["name", "email", "book_title", "author"]
# Register your models here.
