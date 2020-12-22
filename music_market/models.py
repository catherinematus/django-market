from django.db import models
from django.forms import ModelForm


class Product(models.Model):
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    vendor_code = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    country_of_origin = models.CharField(max_length=64)
    warranty = models.IntegerField(blank=True, null=True)
    equipment = models.CharField(max_length=16)
    brand_name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/", verbose_name='Фото', blank=True, null=True)

    def __str__(self):
        return f'{self.product}'


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    subcategory_image = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Basket(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    @property
    def total_price(self):
        total_price = 0
        products_ids = ProductInBasket.objects.filter(basket=self)
        for product in products_ids:
            total_price += product.product.price * product.count
        return total_price

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class ProductInBasket(models.Model):
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def product_totalprice(self):
        return self.product.price * self.count

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзинах'


DELIVERY = (
    ('0', 'Курьером'),
    ('1', 'Почтой'),
    ('2', 'Самовывоз'),
)

PAYMENT = (
    ('0', 'Наличными'),
    ('1', 'Наложенным платежом'),
    ('2', 'Картой онлайн'),
)


class Order(models.Model):
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE)
    order_products = models.CharField(max_length=256, verbose_name='Товары в заказе')
    delivery = models.CharField(max_length=32, choices=DELIVERY, default="0", verbose_name='Доставка')
    payment = models.CharField(max_length=32, choices=PAYMENT, default="0", verbose_name='Оплата')
    user_name = models.CharField(max_length=64, verbose_name="Имя")
    phone = models.CharField(max_length=128, verbose_name="Телефон")

    @property
    def products(self):
        pib = ProductInBasket.objects.filter(basket__id=self.basket.id)
        return pib

    def __str__(self):
        return f'{self.basket.user}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
