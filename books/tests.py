
from django.test import TestCase

from books.models import Book
import pytest
from books.models import Category, Book
from django.urls import reverse
from orders.factories import BookFactory, CategoryFactory


# Create your tests here.

@pytest.mark.django_db
def test_book_str_tittle():
    category = Category.objects.create(
        name="Fantasy",
        slug="fantasy"
    )

    book = Book.objects.create(
        title="Harry Potter",
        author="J. K. Rowling",
        price=100,
        stock=10,
        category=category
    )
    assert book.title == "Harry Potter"
    assert book.author == "J. K. Rowling"
    assert book.price == 100

@pytest.mark.django_db
def test_book_category_relation():
    category = Category.objects.create(
        name="Fantasy",
        slug="fantasy"
    )

    book = Book.objects.create(
        title="Harry Potter",
        author="J. K. Rowling",
        price=100,
        stock=10,
        category=category
    )

    assert book.category.name == "Fantasy"

@pytest.mark.django_db
def test_book_stock():
    category = Category.objects.create(
        name="Fantasy",
        slug="fantasy"
    )

    book = Book.objects.create(
        title="Harry Potter",
        author="J. K. Rowling",
        price=100,
        stock=10,
        category=category
    )

    assert book.stock == 10



@pytest.mark.django_db
def test_all_books_page_opens(client):
    BookFactory.create_batch(3)

    response = client.get(reverse("books:all_books"))

    assert response.status_code == 200

@pytest.mark.django_db
def test_all_books_paginator_opens(client):
    BookFactory.create_batch(4)

    response = client.get(reverse("books:all_books"))
    assert response.status_code == 200
    assert len(response.context["books"]) == 3

@pytest.mark.django_db
def test_book_detail(client):
    book = BookFactory()
    response = client.get(reverse("books:book_detail", kwargs={"pk":book.pk}))
    assert response.status_code == 200
    assert response.context["book"] == book




@pytest.mark.django_db
def test_book_detail_not_found(client):
     book = BookFactory()
     response = client.get(reverse("books:book_detail",kwargs = {"pk":999}))
     assert response.status_code == 404


