from django import forms
from .models import Employee,Product,Customer


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Employee
        fields = ['username', 'first_name','email', 'password','phone_number','address','employee_id','department','position','hire_date','salary']
        labels={"first_name":'Name'}
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        
        }



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'selling_price', 'description', 'brand']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','email','phone', 'city']
