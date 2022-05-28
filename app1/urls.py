from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
   path('',Login,name='Login'),
   path('Register',Register,name='Register'),
   path('ComForgotPass',ComForgotPass,name='ComForgotPass'),
   path('OTP_check',OTP_check,name='OTP_check'),
   path('NewPassword',NewPassword,name='NewPassword'),
   path('DashBoard',DashBoard,name='DashBoard'),
   path('ProfileManage',ProfileManage,name='ProfileManage'),
   path('AddCustomer',AddCustomer,name='AddCustomer'),
   path('ViewCustomer',ViewCustomer,name='ViewCustomer'),
   path('DeleteCustomer/<int:id>',DeleteCustomer,name='DeleteCustomer'),
   path('AddProduct',AddProduct,name='AddProduct'),
   path('ViewProduct',ViewProduct,name='ViewProduct'),
   path('DeleteProducts/<int:id>',DeleteProducts,name='DeleteProducts'),
   path('UpdateProducts/<int:id>',UpdateProducts,name='UpdateProducts'),
   path('ViewOrder',ViewOrder,name='ViewOrder'),
   path('YesOrder/<int:id>',YesOrder,name='YesOrder'),
   path('NoOrder/<int:id>',NoOrder,name='NoOrder'),
   path('MlModule',MlModule,name='MlModule'),
   path('logoutComp',logoutComp,name='logoutComp'),

   path('CustomerLogin',CustomerLogin,name='CustomerLogin'),
   path('CustomerDash',CustomerDash,name='CustomerDash'),
   path('Profile',Profile,name='Profile'),
   path('OrderPlace/<int:id>',OrderPlace,name='OrderPlace'),
   path('AllOrder',AllOrder,name='AllOrder'),
   path('ChatBot',ChatBot,name='ChatBot'),
   path('LogoutCustomer',LogoutCustomer,name='LogoutCustomer'),
]
