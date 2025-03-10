from sqlalchemy import Column, Integer, String, DateTime, Date, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from flask_login import UserMixin
from datetime import datetime

Base = declarative_base()

class TblUserRoles086(Base):
    __tablename__ = 'tbl_user_roles_086'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(10))
    role_sht_name = Column(String(10))
    role_created_date = Column(DateTime, default=datetime.utcnow)
    role_edited_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    users = relationship('TblUsers086', backref='role', lazy=True)

class TblUsers086(Base, UserMixin):
    __tablename__ = 'tbl_users_086'
    usr_idpk = Column(Integer, primary_key=True, autoincrement=True)
    usr_username = Column(String(50), unique=True, nullable=False)
    usr_password = Column(String(256), nullable=False)
    usr_empidfk = Column(Integer, ForeignKey('tbl_employees_086.emp_idpk'))
    usr_roleidfk = Column(Integer, ForeignKey('tbl_user_roles_086.role_id'))
    usr_start_date = Column(DateTime, default=datetime.utcnow)
    usr_end_date = Column(DateTime)
    usr_created_by_userid = Column(Integer)
    usr_edited_by_userid = Column(Integer)
    usr_created_on = Column(DateTime, default=datetime.utcnow)
    usr_edited_on = Column(DateTime, onupdate=datetime.utcnow)

    def get_id(self):
        return str(self.usr_idpk)

class TblEmployees086(Base):
    __tablename__ = 'tbl_employees_086'
    emp_idpk = Column(Integer, primary_key=True, autoincrement=True)
    emp_firstname = Column(String(15), nullable=False)
    emp_lastname = Column(String(15))
    emp_othernames = Column(String(50))
    emp_dob = Column(Date, nullable=False)
    emp_gender_idfk = Column(Integer)
    emp_nationality_idfk = Column(Integer)
    emp_work_status_idfk = Column(Integer)
    emp_marital_status_idfk = Column(Integer)
    emp_email = Column(String(100))
    emp_phone_nos = Column(String(20))
    emp_address_idfk = Column(Integer)
    emp_loyalty_point = Column(Integer)
    emp_job_title_idfk = Column(Integer)
    emp_created_on = Column(DateTime, default=datetime.utcnow)
    emp_edited_on = Column(DateTime, onupdate=datetime.utcnow)
    emp_created_by_user_idfk = Column(String(10))
    emp_edited_by_user_idfk = Column(String(10))
    users = relationship('TblUsers086', backref='employee', lazy=True)

class TblCustomers086(Base):
    __tablename__ = 'tbl_customers_086'
    cus_id = Column(Integer, primary_key=True, autoincrement=True)
    cus_firstname = Column(String(15), nullable=False)
    cus_lastname = Column(String(15), nullable=False)
    cus_othernames = Column(String(50), nullable=False)
    cus_dob = Column(Date, nullable=False)
    cus_gender_idfk = Column(Integer)
    cus_nationality_idfk = Column(Integer)
    cus_marital_status_idfk = Column(Integer)
    cus_occupation = Column(String(30))
    cus_email = Column(String(100), nullable=False)
    cus_phone_nos = Column(String(20))
    cus_address = Column(Text, nullable=False)
    cus_loyalty_points = Column(Integer)
    cus_created_on = Column(DateTime, default=datetime.utcnow)
    cus_edited_on = Column(DateTime, onupdate=datetime.utcnow)
    cus_created_by_user_idfk = Column(String(10))
    cus_edited_by_user_idfk = Column(String(10))
    accounts = relationship('TblAccountDetails086', backref='customer', lazy=True)
    kyc = relationship('TblKyc086', backref='customer', uselist=False, lazy=True)

class TblAccountDetails086(Base):
    __tablename__ = 'tbl_account_details_086'
    acc_account_number = Column(Integer, primary_key=True, autoincrement=True)
    acc_customer_id = Column(Integer, ForeignKey('tbl_customers_086.cus_id'), nullable=False)
    acc_account_type = Column(String(20))
    acc_balance = Column(Numeric(15, 2), nullable=False)
    transactions = relationship('TblTransactions086', backref='account', lazy=True)

class TblKyc086(Base):
    __tablename__ = 'tbl_kyc_086'
    kyc_id = Column(Integer, primary_key=True, autoincrement=True)
    kyc_customer_id = Column(Integer, ForeignKey('tbl_customers_086.cus_id'), nullable=False, unique=True)
    kyc_id_type = Column(String(20))
    kyc_id_number = Column(String(50), nullable=False, unique=True)
    kyc_document_url = Column(String(255))
    kyc_verified_by = Column(Integer)
    kyc_verified_at = Column(DateTime)

class TblTransactions086(Base):
    __tablename__ = 'tbl_transactions_086'
    tst_transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    tst_account_number = Column(Integer, ForeignKey('tbl_account_details_086.acc_account_number'), nullable=False)
    tst_amount = Column(Numeric(15, 2), nullable=False)
    tst_transaction_type = Column(String(20))
    tst_created_by_user_id = Column(Integer)
    tst_created_on = Column(DateTime, default=datetime.utcnow)

class TblAddress086(Base):
    __tablename__ = 'tbl_address_086'
    adr_address_idpk = Column(Integer, primary_key=True, autoincrement=True)
    adr_address = Column(String(50))

class TblCountry086(Base):
    __tablename__ = 'tbl_country_086'
    cty_idpk = Column(Integer, primary_key=True, autoincrement=True)
    cty_name = Column(String(50))
    cty_shortname = Column(String(6))
    cty_nationality = Column(String(50))
    cty_created_by_user_idfk = Column(Integer)
    cty_edited_by_user_idfk = Column(Integer)
    cty_created_on = Column(DateTime)
    cty_edited_on = Column(DateTime)

class TblGender086(Base):
    __tablename__ = 'tbl_gender_086'
    gnd_gender_idpk = Column(Integer, primary_key=True, autoincrement=True)
    gnd_geder_type = Column(String(50))

class TblMaritalStatus086(Base):
    __tablename__ = 'tbl_marital_status_086'
    mts_marital_status_idpk = Column(Integer, primary_key=True, autoincrement=True)
    mts_marital_status_type = Column(String(50))

class TblSecurityLogs086(Base):
    __tablename__ = 'tbl_security_logs_086'
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    log_customer_account_number = Column(Integer)
    log_employee_id = Column(Integer, nullable=False)
    log_action = Column(String(255), nullable=False)
    log_ip_address = Column(String(50))
    log_device_info = Column(String(255))
    log_timestamp = Column(DateTime)
    success = Column(Integer, nullable=False)