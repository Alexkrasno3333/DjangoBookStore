from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db.models import Model
from django.urls import reverse

from books.models import Book
from orders.cart import Cart



# Create your tests here.

from orders.cart import Cart
import pytest

from orders.factories import BookFactory, OrderFactory, OrderItemFactory
from orders.models import Order


class FakeSession(dict):
    modified = False


class FakeRequest:
    def __init__(self):
        self.session = FakeSession()


def test_cart_created():
    request = FakeRequest()
    Cart(request)
    assert request.session["cart"] == {}


def test_add_cart():
    request = FakeRequest()
    cart = Cart(request)
    cart.add_cart(1)
    assert request.session["cart"] == {"1": 1}


def test_remove_cart():
    request = FakeRequest()
    cart = Cart(request)
    cart.add_cart(1)
    assert request.session["cart"] == {"1": 1}
    cart.remove_book_in_cart(1)
    assert request.session["cart"] == {}


def test_plus_cart():
    request = FakeRequest()
    cart = Cart(request)
    cart.add_cart(1)
    assert request.session["cart"] == {"1": 1}
    cart.plus_cart(1)
    assert request.session["cart"] == {"1": 2}


def test_clear_cart():
    request = FakeRequest()
    cart = Cart(request)
    cart.add_cart(1)
    assert request.session["cart"] == {"1": 1}
    cart.clear_cart()
    assert request.session["cart"] == {}


def test_minus_cart():
    request = FakeRequest()
    cart = Cart(request)
    cart.add_cart(1)
    assert request.session["cart"] == {"1": 1}
    cart.add_cart(2)
    assert request.session["cart"] == {"1": 1,"2": 1}
    cart.min_cart(1)
    assert request.session["cart"] == {"2": 1}


def test_min_cart_decreases_quantity():
    request = FakeRequest()
    cart = Cart(request)
    cart.add_cart(1)
    cart.plus_cart(1)
    assert request.session["cart"] == {"1": 2}
    cart.min_cart(1)
    assert request.session["cart"] == {"1": 1}

def test_add_same_book_twice():
    request = FakeRequest()
    cart = Cart(request)

    cart.add_cart(1)
    cart.add_cart(1)

    assert request.session["cart"] == {"1": 2}



def test_remove_not_existing_book_does_not_crash():
    request = FakeRequest()
    cart = Cart(request)

    cart.remove_book_in_cart(999)

    assert request.session["cart"] == {}


def test_min_not_existing_book_does_not_crash():
    request = FakeRequest()
    cart = Cart(request)

    cart.min_cart(999)

    assert request.session["cart"] == {}

@pytest.mark.django_db
def test_order_item_str():
    book = BookFactory()
    book.title = "Test Book"
    assert book.title == "Test Book"

@pytest.mark.django_db
def test_order_item_quantity():
    item = OrderItemFactory(quantity=1,book__price = 10)
    assert item.total_quantity() == 10

@pytest.mark.django_db
def test_order_item_str():
    item = OrderItemFactory(
        book__title="Test Book",
        quantity=2
    )

    assert str(item) == "Test Book x 2"


@pytest.mark.django_db
def test_order_cart_details(client):
   response = client.get(reverse("orders:cart_detail"))
   assert response.status_code == 200

@pytest.mark.django_db
def test_add_cart_details(client):
    book = BookFactory()
    response = client.get(reverse("orders:add_cart",kwargs = {"book_id":book.id}))
    assert response.status_code == 302
    assert client.session["cart"] == {str(book.id): 1}

@pytest.mark.django_db
def test_add_same_book_to_cart_twice(client):
    book = BookFactory()
    client.get(reverse("orders:add_cart",kwargs = {"book_id":book.id}))
    client.get(reverse("orders:add_cart",kwargs = {"book_id":book.id}))
    assert client.session["cart"] == {str(book.id):2}


# mock
@pytest.mark.django_db
@patch("orders.views.send_email.delay")
def test_send_email(mock_delay, client):
    User = get_user_model()
    user = User.objects.create_user(
        username="alex",
        password="password123"
    )

    client.force_login(user)
    book = BookFactory()
    client.get(reverse("orders:add_cart",kwargs = {"book_id":book.id}))
    response = client.post(reverse("orders:checkout"),{
        "name":"alex",
        "phone":123,
        "email":"fndkdk@gmail.com",
    })
    order = Order.objects.first()
    assert response.status_code == 302
    assert order is not None
    mock_delay.assert_called_once_with(order.id)

@pytest.mark.django_db
@patch("orders.views.stripe.checkout.Session.create")
def test_checkout_success(mock_stripe_create,client):
    order = OrderFactory()
    OrderItemFactory(
        order = order,
        book__title = "Test Book",
        quantity = 1,
        price = Decimal("100.00"),

    )
    mock_stripe_create.return_value.url = "https://fake-stripe.com/pay"
    response = client.get(
        reverse("orders:create_checkout_session", kwargs={"order_id": order.id})
    )
    assert response.status_code == 302
    assert response.url == "https://fake-stripe.com/pay"
    mock_stripe_create.assert_called_once()


























