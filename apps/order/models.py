from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from apps.product.models import Product

User = get_user_model()


class Cart(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', related_name='carts')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Общая цена', default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)



class CartItem(models.Model):

    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE, related_name='products')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество продуктов в корзине')
    final_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Общая цена', blank=True, null=True)

    def __str__(self):
        return f'Продукт: {self.product.title} для заказчика {self.cart.owner.email}'



class Order(models.Model):

    STATUS_NEW = 'Новый заказ'
    STATUS_IN_PROGRESS = 'Заказ в обработке'
    STATUS_POSTPONED = 'Отложен'
    STATUS_READY_FOR_DELIVERY = 'Готов к доставке'
    STATUS_PICKED_UP_BY_COURIER = 'Взят курьером'
    STATUS_DELIVERED = 'Доставляется'
    STATUS_COMPLETED = 'Выполнен'
    STATUS_CANCELED = 'Отменен'

    BUYING_TYPE_SELF = 'Самовывоз'
    BUYING_TYPE_DELIVERY = 'Доставка'

    BRANCHE_VEFA = 'Вефа'
    BRANCHE_ASIA_MALL = 'Азия молл'
    BRANCHE_TSUM = 'Цум'
    BRANCHE_BISHKEK_PARK = 'Бишкек парк'

    PAYMENT_IN_CASH = 'Наличными при получении'
    PAYMENT_BY_CREDIT_CARD = 'Оплата банковской картой при получении'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_POSTPONED, 'Отложен'),
        (STATUS_READY_FOR_DELIVERY, 'Готов к доставке'),
        (STATUS_PICKED_UP_BY_COURIER, 'Взят курьером'),
        (STATUS_DELIVERED, 'Доставляется'),
        (STATUS_COMPLETED, 'Выполнен'),
        (STATUS_CANCELED, 'Отменен'),
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка'),
    )

    BRANCHES_CHOICES = (
        (BRANCHE_VEFA, 'Вефа'),
        (BRANCHE_ASIA_MALL, 'Азия молл'),
        (BRANCHE_TSUM, 'Цум'),
        (BRANCHE_BISHKEK_PARK, 'Бишкек парк'),

    )

    PAYMENT_CHOICES = (
        (PAYMENT_IN_CASH, 'Наличными при получении'),
        (PAYMENT_BY_CREDIT_CARD, 'Оплата банковской картой при получении'),
    )


    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель', blank=True, related_name='user_orders')
    name = models.CharField(max_length=100, verbose_name='Имя', blank=True)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', null=True)
    address = models.CharField(max_length=100, verbose_name='Адрес')
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')
    person = models.IntegerField(verbose_name='Сколько персон')
    payment = models.CharField(max_length=100, verbose_name='Тип оплаты', choices=PAYMENT_CHOICES, default=PAYMENT_BY_CREDIT_CARD)
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)
    branch = models.CharField(max_length=100, verbose_name='Филиалы', choices=BRANCHES_CHOICES, default=BRANCHE_VEFA)
    delivery_type = models.CharField(max_length=100, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF)
    comment = models.TextField(verbose_name='Комментарий к заказу', blank=True, null=True)
    create_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateTimeField(default=timezone.now, verbose_name='Дата получения заказа')
    total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, related_name='order_cart', null=True, blank=True)

    street = models.CharField(max_length=100, verbose_name='Улица', blank=True, null=True)
    house = models.CharField(max_length=50, verbose_name='Дом', blank=True, null=True)
    apartment = models.CharField(max_length=50, verbose_name='Квартира', blank=True, null=True)
    entrance = models.CharField(max_length=50, verbose_name='Подъезд', blank=True, null=True)
    intercom = models.CharField(max_length=50, verbose_name='Домофон', blank=True, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField(default=1)
    item_price = models.DecimalField(max_digits=12, decimal_places=2)
