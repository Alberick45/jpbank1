# decorators.py
# jpbankApp/decorators.py
# jpbankApp/views.py
from django.contrib.auth.decorators import login_required
from .decorators import customer_required, admin_required

@login_required
@customer_required
def customer_dashboard(request):
    # Fetch customer-specific data (e.g., accounts)
    accounts = TblAccountDetails086.objects.filter(acc_customer_id=request.user.id)
    return render(request, 'customer_dashboard.html', {'accounts': accounts})

@login_required
@admin_required
def admin_dashboard(request):
    # Fetch admin-specific data (e.g., all users)
    users = CoreUser.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})