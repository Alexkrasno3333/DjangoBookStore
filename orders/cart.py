import orders
from books.models import Book



class Cart:
    def __init__(self, request):
        # запоминаем session пользователя из request типо как шкаф все дела с айди находит ____напоминалка мне
        self.session = request.session

        cart = self.session.get("cart")

        if cart is None:
            cart = {}
            self.session["cart"] = cart

        self.cart = cart

    def save(self):
        self.session.modified = True

    def add_cart(self, book_id):
        book_str = str(book_id)

        if book_str not in self.cart:
            self.cart[book_str] = 1
        else:
            self.cart[book_str] += 1
        self.save()


    def plus_cart(self, book_id):
        book_str = str(book_id)

        if book_str not in self.cart:
            self.cart[book_str] = 1
        else:
            self.cart[book_str] += 1
        self.save()


    def min_cart(self, book_id):
        book_str = str(book_id)

        if book_str in self.cart:
            self.cart[book_str] -= 1

            if self.cart[book_str] <= 0:
                self.remove_book_in_cart(book_id)
            else:
                self.save()


    def clear_cart(self):
        self.session["cart"] = {}
        self.cart = self.session["cart"]
        self.save()


    def remove_book_in_cart(self, book_id):
        book_str = str(book_id)

        if book_str in self.cart:
            del self.cart[book_str]
            self.save()



























