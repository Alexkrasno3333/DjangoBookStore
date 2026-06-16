from multiprocessing import context

from django.shortcuts import render, get_object_or_404, redirect

from books.models import Book
from orders.forms import OrderForm
from orders.models import Order


# Create your views here.
def create_order(request, book_id):
    if not request.user.is_authenticated:
        return redirect("login")

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.book = book
            order.user = request.user

            if order.quantity > book.stock:
                form.add_error("quantity", "Недостаточно книг в наличии")
            else:
                order.save()

                book.stock -= order.quantity
                book.save()

                return redirect("orders:order_success", order_id=order.id)

    else:
        form = OrderForm()

    return render(request, "create_orders.html", {"book": book,"form": form,})

def order_success(request,order_id):
    order = get_object_or_404(Order,id = order_id)
    return render(request,"order_success.html",context={'order':order})


def add_cart(request,book_id):
    book = get_object_or_404(Book,id=book_id)

    cart = request.session.get("cart", {})

    book_str = str(book_id)

    if book_str in cart:
       cart[book_str] += 1
    else:
        cart[book_str] = 1

    request.session["cart"] = cart
    return redirect("books:book_detail", pk=book_id)


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




def delete_cart(request, book_id):
    cart = request.session.get("cart", {})

    book_str = str(book_id)

    if book_str in cart:
        del cart[book_str]

    request.session["cart"] = cart

    return redirect("orders:cart_detail")


def delete_all_cart(request):
    cart = request.session.get("cart", {})
    if cart:
       del cart["cart"]
       request.session["cart"] = {}
    return redirect("orders:cart_detail")
