from flask import Flask
from flask_bcrypt import Bcrypt
from models import db, TblUsers086, TblEmployees086
from datetime import datetime
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# MSSQL Configuration using Windows Authentication
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
db.init_app(app)
bcrypt = Bcrypt(app)

def create_test_data():
    with app.app_context():
        # Create the tables if they don't exist
        db.create_all()
        
        # Check if test user already exists
        if not TblUsers086.query.filter_by(usr_username='admin').first():
            # Create a test employee first
            test_employee = TblEmployees086(
                emp_firstname='Admin',
                emp_lastname='User',
                emp_dob=datetime(1990, 1, 1),
                emp_email='admin@jpbank.com',
                emp_created_on=datetime.now()
            )
            db.session.add(test_employee)
            db.session.flush()  # This will assign the ID to test_employee
            
            # Create test user with hashed password
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            test_user = TblUsers086(
                usr_username='admin',
                usr_password=hashed_password,
                usr_empidfk=test_employee.emp_idpk,
                usr_start_date=datetime.now(),
                usr_created_on=datetime.now()
            )
            db.session.add(test_user)
            
            try:
                db.session.commit()
                print("Test user created successfully!")
                print("Username: admin")
                print("Password: admin123")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating test user: {e}")
        else:
            print("Test user already exists")

if __name__ == '__main__':
    create_test_data()
