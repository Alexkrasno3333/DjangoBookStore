from multiprocessing import context

from django.shortcuts import render, get_object_or_404, redirect

from books.models import Book
from orders.forms import OrderForm
from orders.models import Order, OrderItem
from .cart import Cart
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
import stripe
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import send_email

# Create your views here.

def create_order(request, book_id):
    if not request.user.is_authenticated:
        return redirect("users:login")

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            if book.stock < 1:
                form.add_error(None, "Этой книги нет в наличии")
            else:
                order = form.save(commit=False)
                order.user = request.user
                order.save()

                OrderItem.objects.create(
                    order=order,
                    book=book,
                    quantity=1
                )

                book.stock -= 1
                book.save()

                return redirect("orders:order_success", order_id=order.id)

    else:
        form = OrderForm()

    return render(request, "create_orders.html", {
        "book": book,
        "form": form,
    })

def order_success(request,order_id):
    order = get_object_or_404(Order,id = order_id)
    return render(request,"order_success.html",context={'order':order})


def add_cart(request,book_id):
    cart = Cart(request)
    cart.add_cart(book_id)
    return redirect("books:book_detail", pk=book_id)


def plus_cart(request, book_id):
    cart = Cart(request)
    cart.plus_cart(book_id)
    return redirect("orders:cart_detail")


def min_cart(request, book_id):
    cart = Cart(request)
    cart.min_cart(book_id)

    return redirect("orders:cart_detail")


def delete_cart(request, book_id):
    cart = Cart(request)
    cart.remove_book_in_cart(book_id)

    return redirect("orders:cart_detail")


def delete_all_cart(request):
    cart = Cart(request)
    cart.clear_cart()

    return redirect("orders:cart_detail")


def cart_detail(request):
    cart = request.session.get("cart", {})

    user_all_cart = []
    total = 0

    if cart:
        for key, item in cart.items():
            book = get_object_or_404(Book, id=key)

            total_price = book.price * item
            total += total_price

            user_all_cart.append({
                "book": book,
                "quantity": item,
                "total_price": total_price,
            })

    return render(request, "cart.html", {
        "cart": user_all_cart,
        "total": total,
    })


def checkout(request):
    if not request.user.is_authenticated:
        return redirect("users:login")
    cart = request.session.get("cart", {})
    if not cart :
        return redirect("orders:cart_detail")
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                for key, value in cart.items():
                    book = get_object_or_404(Book, id=key)
                    OrderItem.objects.create(
                        order=order,
                        book=book,
                        quantity=value,
                        price=book.price,
                    )
                request.session["cart"] = {}
                request.session.modified = True
            send_email.delay(order.id)


            return redirect("orders:create_checkout_session", order_id=order.id)
    else:
        form = OrderForm()
    return render(request, "checkout.html", {"form": form})


def create_checkout_session(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    line_items = []

    for item in order.items.all():
        line_items.append({
            "price_data": {
                "currency": "uah",
                "product_data": {
                    "name": item.book.title,
                },
                "unit_amount": int(item.price * 100),
            },
            "quantity": item.quantity,
        })

    success_url = request.build_absolute_uri(
        reverse("orders:order_success", kwargs={"order_id": order.id})
    )

    cancel_url = request.build_absolute_uri(
        reverse("orders:cart_detail")
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=line_items,
        success_url=success_url,
        cancel_url=cancel_url,

    )

    return redirect(session.url, code=303)



# def create_order(request, book_id):
#     if not request.user.is_authenticated:
#         return redirect("users:login")
#
#     book = get_object_or_404(Book, id=book_id)
#
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.book = book
#             order.user = request.user
#
#             if order.quantity > book.stock:
#                 form.add_error("quantity", "Недостаточно книг в наличии")
#             else:
#                 order.save()
#
#                 book.stock -= order.quantity
#                 book.save()
#
#                 return redirect("orders:order_success", order_id=order.id)
#
#     else:
#         form = OrderForm()
#
#     return render(request, "create_orders.html", {"book": book,"form": form,})
#
#     return redirect("orders:cart_detail")
#
# # def add_cart(request,book_id):
# #     book = get_object_or_404(Book,id=book_id)
# #     cart = request.session.get("cart", {})
# #     book_str = str(book_id)
# #
# #     if book_str in cart:
# #        cart[book_str] += 1
# #     else:
# #         cart[book_str] = 1
# #
# #     request.session["cart"] = cart
# #     return redirect("books:book_detail", pk=book_id)
#
#
# # def plus_cart(request, book_id):
# #     cart = request.session.get("cart", {})
# #     book_id = str(book_id)
# #
# #     if book_id in cart:
# #         cart[book_id] += 1
# #     else:
# #         cart[book_id] = 1
# #
# #     request.session["cart"] = cart
# #
# #     return redirect("orders:cart_detail")
#
#
# def min_cart(request,book_id):
#     cart = request.session.get("cart", {})
#     book = get_object_or_404(Book,id=book_id)
#     book_str = str(book_id)
#
#     if book_str in cart:
#         cart[book_str] -= 1
#     if cart[book_str] == 0:
#         del cart[book_str]
#     request.session["cart"] = cart
#
#     return redirect("orders:cart_detail")
#
#
# def delete_cart(request, book_id):
#     cart = request.session.get("cart", {})
#
#     book_str = str(book_id)
#
#     if book_str in cart:
#         del cart[book_str]
#
#     request.session["cart"] = cart
#
#     return redirect("orders:cart_detail")
#
#
# def delete_all_cart(request):
#     cart = request.session.get("cart", {})
#     if cart:
#        request.session["cart"] = {}
#     return redirect("orders:cart_detail")


