from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
STATE_CHOICES = (("sen", "senegal"), ("cot", "code ivour"),
                 ("mali", "Mali"), ("Gam", "Gambia"), ("Brf", "Bourkina Fassau"))


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    lacality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


GATEGORY_CHOICES = (("M", "Mobile"), ("PC", "Laptop"),
                    ("IP", "Ipate"), ("AC", "Accesoires"))


class Product(models.Model):
    title = models.CharField(max_length=50)
    selling_price = models.FloatField()

    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=GATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to="product_img")

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price


STATUS_CHOICES = (("Accepted", "Accepted"), ("Packet", "Packet"),
                  ("On The Way", "On The Way"), ("Delivered", "Delivered"), ("Cancel", "Cancel"))


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default=" Non Commencé")

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price
