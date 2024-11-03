from django.db import models
import datetime
from django.contrib.auth.models import User as AuthUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField

class UserProfile(models.Model):  # Extended User model
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10,default = '9999999999', unique=True)
    is_plus_member = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

# @receiver(post_save, sender=AuthUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=AuthUser)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()

class Cart(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name

class Seller(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=255, null=False)
    account_id = models.BigIntegerField(null=False, unique=True)

    def __str__(self):
        return self.seller_name

class Product(models.Model):
    product_name = models.CharField(max_length=255, null=False)
    product_price = models.DecimalField(null=False, decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    discount = models.BigIntegerField(default=0)
    product_description = RichTextField(default="No description available")
    img = models.ImageField(upload_to='uploads/product/')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.product_name


class ProductsSellers(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

class Order(models.Model):
    order_total = models.DecimalField(null=False, decimal_places=2, max_digits=8)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

class UserOrders(models.Model):  # Renamed for consistency
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class OrdersProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.BigIntegerField(default=1)

class Address(models.Model):
    house_no = models.CharField(max_length=15,null=False)
    street_name = models.CharField(max_length=255, default="Unknown")
    address_lines = models.TextField(null=False)
    city = models.CharField(max_length=255, null=False)
    region = models.CharField(max_length=255, null=False)
    pincode = models.BigIntegerField(null=False)

class UserAddresses(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.BigIntegerField(default=1)
