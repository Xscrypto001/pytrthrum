# ecommerce_app/models.py

from django.db import models
from django.contrib.auth.models import User
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Services(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    Approval = models.BooleanField(default=False,null=True)

    

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)

class Order_product(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True , null=True)
    quantity = models.IntegerField()


    
    
class Order_Services(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    services = models.ForeignKey(Services, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=100)
    description = models.TextField()
    Approval = models.BooleanField(default=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
