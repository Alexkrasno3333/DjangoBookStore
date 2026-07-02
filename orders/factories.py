import factory
from books.models import Category, Book
from orders.models import Order, OrderItem


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"Category {n}")



class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
    title = factory.Sequence(lambda n: f"Book {n}")
    author = "Test Author"
    price = 100
    stock = 10
    category = factory.SubFactory(CategoryFactory)

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    name = "Alex"
    phone = "0991112233"
    email = "test@example.com"


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    book = factory.SubFactory(BookFactory)
    quantity = 3
    price = 100


