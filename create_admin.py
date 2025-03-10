from app import app, db
from models import TblUsers086, TblEmployees086, TblUserRoles086
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_admin_user():
    with app.app_context():
        # Check if admin role exists
        admin_role = TblUserRoles086.query.filter_by(role_name='Admin').first()
        if not admin_role:
            admin_role = TblUserRoles086(
                role_name='Admin',
                role_sht_name='ADM',
                role_created_date=datetime.utcnow()
            )
            db.session.add(admin_role)
            db.session.flush()

        # Create admin employee
        admin_employee = TblEmployees086(
            emp_firstname='Admin',
            emp_lastname='User',
            emp_email='admin@jpbank.com',
            emp_dob=datetime(1990, 1, 1)  # Default date of birth
        )
        db.session.add(admin_employee)
        db.session.flush()

        # Create admin user
        admin_user = TblUsers086(
            usr_username='admin',
            usr_password=generate_password_hash('admin123'),
            usr_empidfk=admin_employee.emp_idpk,
            usr_roleidfk=admin_role.role_id,
            usr_start_date=datetime.utcnow()
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")

if __name__ == '__main__':
    create_admin_user()
