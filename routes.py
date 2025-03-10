""" from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager
import bcrypt
from datetime import datetime
from models import (
    TblUsers086, TblEmployees086, TblCustomers086, 
    TblAccountDetails086, TblKyc086, TblTransactions086
)

@login_manager.user_loader
def load_user(user_id):
    return TblUsers086.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = TblUsers086.query.filter_by(usr_username=username).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.usr_password.encode('utf-8')):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if hasattr(current_user, 'usr_empidfk'):
        employee = TblEmployees086.query.get(current_user.usr_empidfk)
        return render_template('dashboard.html', employee=employee)
    return render_template('dashboard.html')

@app.route('/customers')
@login_required
def customers():
    customers = TblCustomers086.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/customer/<int:customer_id>')
@login_required
def customer_details(customer_id):
    customer = TblCustomers086.query.get_or_404(customer_id)
    accounts = TblAccountDetails086.query.filter_by(acc_customer_id=customer_id).all()
    kyc = TblKyc086.query.filter_by(kyc_customer_id=customer_id).first()
    return render_template('customer_details.html', customer=customer, accounts=accounts, kyc=kyc)

@app.route('/transactions')
@login_required
def transactions():
    transactions = TblTransactions086.query.order_by(TblTransactions086.tst_created_on.desc()).limit(100)
    return render_template('transactions.html', transactions=transactions)

@app.route('/transaction/new', methods=['GET', 'POST'])
@login_required
def new_transaction():
    if request.method == 'POST':
        account_number = request.form.get('account_number')
        amount = request.form.get('amount')
        transaction_type = request.form.get('transaction_type')
        
        try:
            account = TblAccountDetails086.query.filter_by(acc_account_number=account_number).first()
            if not account:
                flash('Account not found')
                return redirect(url_for('new_transaction'))
                
            amount = float(amount)
            if transaction_type == 'withdrawal' and account.acc_balance < amount:
                flash('Insufficient funds')
                return redirect(url_for('new_transaction'))
                
            transaction = TblTransactions086(
                tst_account_number=account_number,
                tst_amount=amount,
                tst_transaction_type=transaction_type,
                tst_created_by_user_id=current_user.usr_idpk,
                tst_created_on=datetime.now()
            )
            
            if transaction_type == 'deposit':
                account.acc_balance += amount
            else:
                account.acc_balance -= amount
                
            db.session.add(transaction)
            db.session.commit()
            
            flash('Transaction completed successfully')
            return redirect(url_for('transactions'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error processing transaction')
            
    return render_template('new_transaction.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('index'))














    from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv
import pyodbc
import urllib.parse

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change')

# MSSQL Configuration
server = os.getenv('DB_SERVER', 'localhost')
database = os.getenv('DB_NAME', 'jpbank086')
driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
trusted_connection = os.getenv('DB_TRUSTED_CONNECTION', 'yes')

# Create the connection string for Windows Authentication
params = urllib.parse.quote_plus(
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection={trusted_connection};'
)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Import routes after everything else
import routes

if __name__ == '__main__':
    app.run(debug=True)

 """