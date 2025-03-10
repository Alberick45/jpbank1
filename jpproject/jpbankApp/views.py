# jpbankApp/views.py
from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm, AdminRegistrationForm

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register_customer.html', {'form': form})

def register_admin(request):
    # Similar to register_customer, but uses AdminRegistrationForm
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'register_admin.html', {'form': form})