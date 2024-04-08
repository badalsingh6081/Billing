from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect
from rest_framework.response import Response
from .forms import ProductForm,CustomerForm 
from .models import Product,Customer,Order,Employee
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from  django.contrib.auth.decorators import login_required
from .forms import RegistrationForm



def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('api/login')  # Redirect to success page after registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
    





def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/api/')  # Redirect to home page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('home')  # Redirect to login page after logout












def add_product(request):
  
  if request.user.is_authenticated:    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/api/add_product/')  # Redirect to product list page after successful form submission
    else:
        form = ProductForm()
        products = Product.objects.all()
    return render(request, 'add_product.html', {'form': form,'products': products})
  else:
      return render(request,'login.html')


def delete_product(request, product_id):
  
  if request.user.is_authenticated:    
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('/api/add_product/')  # Redirect to product list page after deletion
    return render(request, 'delete_product.html', {'product': product})
  else:
      return render(request,'login.html')


def update_product(request, product_id):
  
  if request.user.is_authenticated:    
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/api/add_product/')  # Redirect to product list page after update
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form, 'product': product})
  else:
      return render(request,'login.html')










def add_customer(request):
  
  if request.user.is_authenticated:    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/api/add_customer/')  # Redirect to customer list page after successful form submission
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})
  else:
      return render(request,'login.html')


def delete_customer(request, customer_id):
  
  if request.user.is_authenticated:    
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('/api/add_customer/')  # Redirect to customer list page after deletion
    return render(request, 'delete_customer.html', {'customer': customer})
  else:
      return render(request,'login.html')


def update_customer(request, customer_id):
  
  if request.user.is_authenticated:    
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/api/add_customer/')  # Redirect to customer list page after update
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'update_customer.html', {'form': form, 'customer': customer})
  else:
      return render(request,'login.html')


def billing(request):
  
  if request.user.is_authenticated:    
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        customer_city = request.POST.get('customer_city')
        selected_products = request.POST.getlist('selected_products')

        # Fetch customer or create a new one
        customer, created = Customer.objects.get_or_create(
            name=customer_name,
            email=customer_email,
            phone=customer_phone,
            city=customer_city
        )

        # Fetch selected products
        products = Product.objects.filter(id__in=selected_products)

        # Calculate total amount
        total_amount = sum([product.selling_price for product in products])

        # Create order
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount
        )
        order.products.set(products)

        return render(request, 'billing.html', {'order': order})
    else:
        products = Product.objects.all()
        return render(request, 'select_products.html', {'products': products})
  else:
      return render(request,'login.html') 
  


# ------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
# Django rest framework code


from .serializers import Productserializer,Customerserializer,EmployeeLoginserializer
from . models import Product,Customer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,ListModelMixin
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# product views

class Product_list(GenericAPIView,ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    
    

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

class Product_create(GenericAPIView,CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    

    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
class Product_retrieve(GenericAPIView,RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    
    

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

class Product_update(GenericAPIView,UpdateModelMixin):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    
    

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

class Product_destroy(GenericAPIView,DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    
    

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


# customer views


class Customer_list(GenericAPIView,ListModelMixin):
    queryset = Customer.objects.all()
    serializer_class = Customerserializer
    
    

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    

class Customer_create(GenericAPIView,CreateModelMixin):
    queryset = Customer.objects.all()
    serializer_class = Customerserializer
    
    

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
class Customer_retrieve(GenericAPIView,RetrieveModelMixin):
    queryset = Customer.objects.all()
    serializer_class = Customerserializer
    
    

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

class Customer_update(GenericAPIView,UpdateModelMixin):
    queryset = Customer.objects.all()
    serializer_class = Customerserializer
    
    

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

class Customer_destroy(GenericAPIView,DestroyModelMixin):
    queryset = Customer.objects.all()
    serializer_class = Customerserializer
    
    

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


class  EmployeeLoginView(APIView):
    def post(self,request,format=None):
        serializer=EmployeeLoginserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username=serializer.data.get('username')
            password=serializer.data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
              token=get_tokens_for_user(user)
              return Response({'token':token,'msg':'Login Success'},content_type='application/json')
        # return HttpResponse(json_data,content_type='application/json'))    
        return Response(serializer.errors)    

