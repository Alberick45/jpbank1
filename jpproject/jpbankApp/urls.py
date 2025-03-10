# jpbank/urls.py
from django.urls import path
from jpbankApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/admin/', views.register_admin, name='register_admin'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]