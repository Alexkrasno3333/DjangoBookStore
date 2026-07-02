from django.db import models

from books.models import Book
from djangobookstore import settings
from users.forms import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("User")
    )
    name = models.CharField(_("Name"), max_length=100)
    phone = models.CharField(_("Phone"), max_length=100)
    email = models.EmailField(_("Email"), blank=True, null=True)
    is_paid = models.BooleanField(_("Is paid"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    stripe_checkout_session_id = models.CharField(
        _("Stripe checkout session ID"),
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{_('Order')} #{self.id}"

    def total_price(self):
        total_price = 0
        for i in self.items.all():
            total_price += i.total_quantity()
        return total_price

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items",verbose_name=_("Order"))
    book = models.ForeignKey(Book,on_delete=models.CASCADE,verbose_name=_("Book"))
    quantity = models.PositiveIntegerField(_("Quantity"),default=1)
    price = models.DecimalField(_("Price"),max_digits=10,decimal_places=2)

    def total_quantity(self):
        return self.quantity * self.book.price

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")