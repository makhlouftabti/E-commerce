from django.db import migrations, models
from django.contrib.auth.models import User


# Create your models here.


# Customer
class Customer(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=10, null=True)
    avatar = models.ImageField(blank=True, null=True, default="preson.png")
    balance = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


# Brand


class Brand(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name


# Product
class Product(models.Model):
    GENDER = (("male", "male"), ("female", "female"))
    name = models.CharField(max_length=20)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    gender = models.CharField(max_length=15, choices=GENDER)
    picture = models.ImageField(null=False)
    description = models.TextField()

    def __str__(self):
        return self.name


# Cart
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartItem")

    def total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.subtotal()
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    total = models.IntegerField(default=0)
