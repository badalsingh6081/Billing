# admin.py

from django.contrib import admin
from .models import Customer, Product, Employee,Order

# Register Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','name','email', 'phone' ,'city']

# Register Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'selling_price', 'description','brand']

# Register Employee model
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'first_name', 'last_name', 'email', 'department', 'position', 'hire_date', 'salary']
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'get_product_names', 'total_amount')

    def get_product_names(self, obj):
        return ", ".join([product.name for product in obj.products.all()])

    get_product_names.short_description = 'Products'

