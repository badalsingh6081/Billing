
from rest_framework import serializers
from .models import Product,Customer,Employee

class Productserializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['id','name', 'selling_price', 'description','brand']


class Customerserializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields = ['id','name','email', 'phone' ,'city']

class EmployeeLoginserializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=200)
    class Meta:
        model=Employee
        fields = ['username','password']
