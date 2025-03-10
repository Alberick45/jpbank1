from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import urllib
from dotenv import load_dotenv
from functools import wraps
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base, TblUsers086, TblEmployees086, TblUserRoles086

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

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = db.query(TblUsers086).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/roles')
@login_required
@admin_required
def admin_roles():
    roles = db.query(TblUserRoles086).all()
    return render_template('admin/roles.html', roles=roles)

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