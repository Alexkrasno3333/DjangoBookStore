from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Category(models.Model):
    name = models.CharField(_("Name"),max_length=100)
    slug = models.SlugField(_("Slug"),max_length=100, unique=True)
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Book(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name=_("Category")
    )
    title = models.CharField(_("Title"), max_length=200)
    author = models.CharField(_("Author"), max_length=200)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    description = models.TextField(_("Description"), blank=True)
    stock = models.PositiveIntegerField(_("Stock"))

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")


class BookSuggestion(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    book_title = models.CharField(max_length=200)
    author = models.CharField(max_length=150, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_title

