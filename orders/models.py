from django.db import models

from books.models import Book
from djangobookstore import settings
from users.forms import User


# Create your models here.


class Order(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True,
    blank=True)
    name = models.CharField( max_length=100)
    phone = models.CharField( max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=0,verbose_name="Количество")

    def total_quantity(self):
        return self.quantity * self.book.price

    def __str__(self):
        return  f"Заказ #{self.id} - {self.book.title}"



