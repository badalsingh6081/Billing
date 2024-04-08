# urls.py

from django.urls import path
from .views import add_customer,add_product,delete_product,update_product,delete_customer,update_customer,Login,Logout,billing,home,EmployeeLoginView,register,Product_create,Product_destroy,Product_retrieve,Product_update,Customer_create,Customer_destroy, Customer_retrieve,Customer_update,Product_list,Customer_list
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView


from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Billing System",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@xyz.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('add_product/', add_product, name='add_product'),
    path('product/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('product/update/<int:product_id>/', update_product, name='update_product'),

    path('add_customer/', add_customer, name='add_customer'),
    path('customer/delete/<int:customer_id>/', delete_customer, name='delete_customer'),
    path('customer/update/<int:customer_id>/', update_customer, name='update_customer'),
    
    path('billing/', billing, name='billing'),
     
    path('',home, name='home'), 
    path('register/', register, name='register'),


    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),



    # drf
    path('authenticate/', EmployeeLoginView.as_view()),
    

    path('customer_list/', Customer_list.as_view()),
    path('customer_create/', Customer_create.as_view()),
    path('customer_retrieve/<int:pk>', Customer_retrieve.as_view()),
    path('customer_update/<int:pk>', Customer_update.as_view()),
    path('customer_destroy/<int:pk>', Customer_destroy.as_view()),

    path('product_list/', Product_list.as_view()),
    path('product_create/', Product_create.as_view()),
    path('product_retrieve/<int:pk>', Product_retrieve.as_view()),
    path('product_update/<int:pk>', Product_update.as_view()),
    path('product_destroy/<int:pk>', Product_destroy.as_view()),


    path('gettoken/',TokenObtainPairView.as_view(),name='gettoken'),
    path('refreshtoken/',TokenRefreshView.as_view(),name='refreshtoken'),
    path('verifytoken/',TokenVerifyView.as_view(),name='verifytoken'),


    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

