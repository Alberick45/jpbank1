from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import urllib
from dotenv import load_dotenv
from functools import wraps
from urllib.parse import urlparse
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import scoped_session, sessionmaker
from decimal import Decimal
from models import Base, TblUsers086, TblEmployees086, TblUserRoles086, TblCustomers086, TblAccountDetails086, TblTransactions086, TblSecurityLogs086
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Database configuration
params = urllib.parse.quote_plus(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={os.getenv("DB_SERVER", "localhost")};'
    f'DATABASE={os.getenv("DB_NAME", "jpbank086")};'
    f'Trusted_Connection={os.getenv("DB_TRUSTED_CONNECTION", "yes")}'
)

# Create engine and session
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
db = scoped_session(sessionmaker(bind=engine))

# Create all tables
Base.metadata.create_all(engine)

# Login manager configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return db.query(TblUsers086).get(int(user_id))

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            role = db.query(TblUserRoles086).filter_by(role_name=role_name).first()
            if current_user.usr_roleidfk != role.role_id:
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.role or current_user.role.role_name != 'Admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return render_template('login.html')
        
        user = db.query(TblUsers086).filter_by(usr_username=username).first()
        
        if user and check_password_hash(user.usr_password, password):
            if user.usr_end_date:
                flash('Your account has been deactivated. Please contact an administrator.', 'danger')
                return render_template('login.html')
            
            login_user(user)
            next_page = request.args.get('next')
            
            flash(f'Welcome back, {user.employee.emp_firstname}!', 'success')
            
            if next_page and urlparse(next_page).netloc == '':
                return redirect(next_page)
            return redirect(url_for('index'))
        
        flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        dob = request.form.get('dob')
        
        try:
            # Check if username already exists
            if db.query(TblUsers086).filter_by(usr_username=username).first():
                flash('Username already exists.', 'danger')
                return render_template('signup.html', now=datetime.now(), timedelta=timedelta)
            
            # Create employee record
            employee = TblEmployees086(
                emp_firstname=firstname,
                emp_lastname=lastname,
                emp_email=email,
                emp_dob=datetime.strptime(dob, '%Y-%m-%d')
            )
            db.add(employee)
            db.flush()
            
            # Get Teller role
            teller_role = db.query(TblUserRoles086).filter_by(role_name='Teller').first()
            if not teller_role:
                teller_role = TblUserRoles086(
                    role_name='Teller',
                    role_sht_name='TLR',
                    role_created_date=datetime.utcnow()
                )
                db.add(teller_role)
                db.flush()
            
            # Create user record
            user = TblUsers086(
                usr_username=username,
                usr_password=generate_password_hash(password),
                usr_empidfk=employee.emp_idpk,
                usr_roleidfk=teller_role.role_id,
                usr_start_date=datetime.utcnow()
            )
            db.add(user)
            db.commit()
            
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.rollback()
            flash('An error occurred while creating your account.', 'danger')
            return render_template('signup.html', now=datetime.now(), timedelta=timedelta)
    
    return render_template('signup.html', now=datetime.now(), timedelta=timedelta)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Teller Transaction Routes
@app.route('/teller/transactions')
@login_required
@role_required('Teller')
def teller_transactions():
    transactions = db.query(TblTransactions086).all()
    return render_template('transactions.html', transactions=transactions)

@app.route('/new_transaction', methods=['GET', 'POST'])
@login_required
@role_required('Teller')
def new_transaction():
    if request.method == 'POST':
        account_number = request.form.get('account_number')
        amount = request.form.get('amount')
        transaction_type = request.form.get('transaction_type')

        try:
            # Convert amount to Decimal for precise handling
            amount = Decimal(str(amount))
            
            # Validate account exists
            account = db.query(TblAccountDetails086).get(account_number)
            if not account:
                flash('Account not found.', 'danger')
                return redirect(url_for('new_transaction'))

            # Convert account balance to Decimal for comparison
            current_balance = Decimal(str(account.acc_balance))

            # Validate sufficient funds for withdrawal
            if transaction_type == 'withdrawal':
                if amount > current_balance:
                    flash('Insufficient funds.', 'danger')
                    return redirect(url_for('new_transaction'))

            # Create transaction record
            transaction = TblTransactions086(
                tst_account_number=account_number,
                tst_amount=amount,
                tst_transaction_type=transaction_type,
                tst_created_by_user_id=current_user.usr_idpk
            )
            db.add(transaction)

            # Update account balance using Decimal arithmetic
            if transaction_type == 'deposit':
                account.acc_balance = current_balance + amount
            else:  # withdrawal
                account.acc_balance = current_balance - amount

            # Log the security event
            security_log = TblSecurityLogs086(
                log_customer_account_number=account_number,
                log_employee_id=current_user.usr_empidfk,
                log_action=f"{transaction_type.capitalize()} of ${amount:.2f}",
                log_ip_address=request.remote_addr,
                log_device_info=request.user_agent.string,
                log_timestamp=datetime.utcnow(),
                success=1
            )
            db.add(security_log)

            db.commit()
            flash(f'{transaction_type.capitalize()} of ${amount:.2f} completed successfully.', 'success')
            return redirect(url_for('teller_transactions'))

        except ValueError:
            db.rollback()
            flash('Invalid amount format. Please enter a valid number.', 'danger')
            return redirect(url_for('new_transaction'))
        except Exception as e:
            db.rollback()
            flash('Error processing transaction. Please try again.', 'danger')
            return redirect(url_for('new_transaction'))

    return render_template('new_transaction.html')

@app.route('/teller/account/<int:account_number>')
@login_required
@role_required('Teller')
def account_details(account_number):
    account = db.query(TblAccountDetails086).filter_by(acc_account_number=account_number).first()
    if not account:
        flash('Account not found.', 'danger')
        return redirect(url_for('teller_transactions'))
    
    transactions = db.query(TblTransactions086).filter_by(tst_account_number=account_number).order_by(desc(TblTransactions086.tst_created_on)).all()
    return render_template('teller/account_details.html', account=account, transactions=transactions)

# Teller Account Management Routes
@app.route('/teller/accounts')
@login_required
@role_required('Teller')
def customer_accounts():
    accounts = db.query(TblAccountDetails086)\
        .join(TblCustomers086)\
        .add_columns(
            TblCustomers086.cus_firstname,
            TblCustomers086.cus_lastname,
            TblCustomers086.cus_email,
            TblAccountDetails086.acc_account_number,
            TblAccountDetails086.acc_account_type,
            TblAccountDetails086.acc_balance
        ).all()
    
    return render_template('teller/accounts.html', accounts=accounts)

@app.route('/teller/account/<int:account_number>')
@login_required
@role_required('Teller')
def account_details_teller(account_number):
    # Get account details with customer information
    account = db.query(TblAccountDetails086)\
        .join(TblCustomers086)\
        .filter(TblAccountDetails086.acc_account_number == account_number)\
        .add_columns(
            TblCustomers086.cus_firstname,
            TblCustomers086.cus_lastname,
            TblCustomers086.cus_email,
            TblCustomers086.cus_phone_nos,
            TblAccountDetails086.acc_account_number,
            TblAccountDetails086.acc_account_type,
            TblAccountDetails086.acc_balance
        ).first_or_404()
    
    # Get recent transactions for this account
    transactions = db.query(TblTransactions086)\
        .filter_by(tst_account_number=account_number)\
        .order_by(desc(TblTransactions086.tst_created_on))\
        .limit(10)\
        .all()
    
    return render_template('teller/account_details.html', account=account, transactions=transactions)

# Admin User Management Routes
@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = db.query(TblUsers086).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = db.query(TblUsers086).filter_by(usr_idpk=user_id).first()
    if not user:
        abort(404)
    
    if request.method == 'POST':
        try:
            user.usr_username = request.form['username']
            user.usr_roleidfk = int(request.form['role_id'])
            user.usr_edited_on = datetime.utcnow()
            db.commit()
            flash('User updated successfully', 'success')
            return redirect(url_for('manage_users'))
        except Exception as e:
            db.rollback()
            flash(f'Update failed: {str(e)}', 'danger')
    
    roles = db.query(TblUserRoles086).all()
    return render_template('admin/edit_user.html', user=user, roles=roles)


#accountant

@app.route('/accountant')
@login_required
@role_required('Accountant')
def accountant_dashboard():
    # Get customers for the dashboard
    customers = db.query(TblCustomers086).all()
    return render_template('accountant/dashboard.html', customers=customers)

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            
            user = db.query(TblUsers086).filter_by(usr_idpk=current_user.usr_idpk).first()
            role = db.query(TblUserRoles086).filter_by(role_id=user.usr_roleidfk).first()
            
            if role.role_name != role_name:
                flash(f'Access denied. {role_name} role required.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/new_customer', methods=['GET', 'POST'])
@login_required
@role_required('Accountant')
def new_customer():
    if request.method == 'POST':
        customer = TblCustomers086(
            cus_firstname=request.form['firstname'],
            cus_lastname=request.form['lastname'],
            cus_othernames=request.form['othernames'],
            cus_dob=datetime.strptime(request.form['dob'], '%Y-%m-%d'),
            cus_email=request.form['email'],
            cus_phone_nos=request.form['phone'],
            cus_address=request.form['address']
        )
        db.add(customer)
        db.commit()
        flash('Customer added successfully', 'success')
        return redirect(url_for('customers'))
    return render_template('new_customer.html')


@app.route('/admin/user/toggle/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_user(user_id):
    user = db.query(TblUsers086).filter_by(usr_idpk=user_id).first()
    if not user:
        abort(404)
        
    try:
        user.usr_is_active = not user.usr_is_active
        db.commit()
        status = "activated" if user.usr_is_active else "deactivated"
        db.commit()
        flash(f'User {status} successfully.', 'success')
    except Exception as e:
        db.rollback()
        flash('Error toggling user status. Please try again.', 'danger')
    return redirect(url_for('admin_users'))

# Admin Role Management Routes
@app.route('/admin/roles')
@login_required
@admin_required
def admin_roles():
    roles = db.query(TblUserRoles086).all()
    return render_template('admin/roles.html', roles=roles)

@app.route('/admin/role/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_role():
    if request.method == 'POST':
        new_role = TblUserRoles086(
            role_name=request.form['role_name'],
            role_sht_name=request.form['role_sht_name'],
            role_created_date=datetime.utcnow()
        )
        db.session.add(new_role)
        db.session.commit()
        flash('New role created successfully', 'success')
        return redirect(url_for('roles'))
    return render_template('admin/new_role.html')

@app.route('/admin/role/edit/<int:role_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_role():
    role = TblUserRoles086.query.get_or_404(role_id)
    if request.method == 'POST':
        role.role_name = request.form['role_name']
        role.role_sht_name = request.form['role_sht_name']
        role.role_edited_date = datetime.utcnow()
        db.session.commit()
        flash('Role updated successfully', 'success')
        return redirect(url_for('roles'))
    return render_template('admin/edit_role.html', role=role)

@app.route('/profile')
@login_required
def profile():
    user = db.query(TblUsers086).filter_by(usr_idpk=current_user.usr_idpk).first()
    employee = None
    if user.usr_empidfk:
        employee = db.query(TblEmployees086).filter_by(emp_idpk=user.usr_empidfk).first()
    return render_template('profile.html', user=user, employee=employee)


@app.route('/admin/role/delete/<int:role_id>', methods=['POST'])
@login_required
@admin_required
def delete_role(role_id):
    role = db.query(TblUserRoles086).filter_by(role_id=role_id).first()
    if not role:
        abort(404)
    
    # Prevent deletion of core roles
    if role.role_name in ['Admin', 'Teller']:
        flash('Cannot delete core system roles.', 'danger')
        return redirect(url_for('admin_roles'))
    
    try:
        # Check if role is assigned to any users
        users_with_role = db.query(TblUsers086).filter_by(usr_roleidfk=role_id).count()
        if users_with_role > 0:
            flash('Cannot delete role that is assigned to users. Please reassign users first.', 'danger')
            return redirect(url_for('admin_roles'))
        
        # Log the deletion
        security_log = TblSecurityLogs086(
            log_employee_id=current_user.usr_empidfk,
            log_action=f"Deleted role: {role.role_name}",
            log_ip_address=request.remote_addr,
            log_device_info=request.user_agent.string,
            log_timestamp=datetime.utcnow(),
            success=1
        )
        db.add(security_log)
        
        # Delete the role
        db.delete(role)
        db.commit()
        
        flash('Role deleted successfully.', 'success')
    except Exception as e:
        db.rollback()
        flash('Error deleting role. Please try again.', 'danger')
    
    return redirect(url_for('admin_roles'))

if __name__ == '__main__':
    # Create default roles if they don't exist
    admin_role = db.query(TblUserRoles086).filter_by(role_name='Admin').first()
    if not admin_role:
        admin_role = TblUserRoles086(
            role_name='Admin',
            role_sht_name='ADM'
        )
        db.add(admin_role)
    
    teller_role = db.query(TblUserRoles086).filter_by(role_name='Teller').first()
    if not teller_role:
        teller_role = TblUserRoles086(
            role_name='Teller',
            role_sht_name='TLR'
        )
        db.add(teller_role)
    
    db.commit()
    
    app.run(debug=True)