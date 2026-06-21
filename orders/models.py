from django.db import models

from books.models import Book
from djangobookstore import settings
from users.forms import User


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField( max_length=100)
    phone = models.CharField( max_length=100)
    email = models.EmailField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_checkout_session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return  f"Заказ #{self.id}"

    def total_price(self):
        total_price = 0
        for i in self.items.all():
            total_price += i.total_quantity()
        return total_price




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def total_quantity(self):
        return self.quantity * self.book.price

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

