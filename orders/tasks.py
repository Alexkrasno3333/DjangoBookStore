from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def send_email(order_id):
    order = Order.objects.get(id=order_id)
    send_mail(
        subject=f"Заказ #{order.id} создан",
        message=f"Спасибо за заказ! Ваш заказ #{order.id} успешно создан.",
        from_email=None,
        recipient_list=[order.email],
        fail_silently=False,
    )

