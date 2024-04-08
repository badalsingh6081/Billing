from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    name=models.CharField(max_length=200)
    email = models.EmailField()
    phone=models.CharField(max_length=200)
    city=models.CharField(max_length=50)





class Product(models.Model):
    name=models.CharField(max_length=100)
    selling_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order for {self.customer.name}"








class Employee(User):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.username

    

