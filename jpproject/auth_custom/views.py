from django.shortcuts import render

# Create your views here.
from .models import TblUsers086, UserRole
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        created_by_userid = 1
        edited_by_userid = 1
        start_date = datetime.datetime.now()
        user = TblUsers086.objects.create(usr_username=username, usr_password=password, usr_created_by_userid=created_by_userid, usr_edited_by_userid=edited_by_userid, usr_start_date=start_date)
        user.save()
        return HttpResponse('User created successfully')
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('User logged in successfully')
        else:
            return HttpResponse('Invalid credentials')
    return render(request, 'login.html')

def get_user_roles(request):
    user = request.user
    user_roles = UserRole.objects.filter(user=user)
    return render(request, 'user_roles.html', {'user_roles': user_roles})

#decorator for roles
def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user_roles = UserRole.objects.filter(user=request.user)
            for role in user_roles:
                if role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

@role_required(allowed_roles=['admin'])
def home(request):
    return HttpResponse('Home page')

def logout(request):
    return HttpResponse('Logout page')