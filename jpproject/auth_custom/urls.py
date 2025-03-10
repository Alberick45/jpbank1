from django.urls import path
from auth import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user_roles/', views.get_user_roles, name='user_roles'),
    path('home/', views.home, name='home'),
]