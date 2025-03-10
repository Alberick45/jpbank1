-- Create User Roles Table
CREATE TABLE tbl_user_roles_086 (
    role_id INT IDENTITY(1,1) PRIMARY KEY,
    role_name VARCHAR(10),
    role_sht_name VARCHAR(10),
    role_created_date DATETIME,
    role_edited_date DATETIME
);

-- Create Employees Table
CREATE TABLE tbl_employees_086 (
    emp_idpk INT IDENTITY(1,1) PRIMARY KEY,
    emp_firstname VARCHAR(15) NOT NULL,
    emp_lastname VARCHAR(15),
    emp_othernames VARCHAR(50),
    emp_dob DATE NOT NULL,
    emp_gender_idfk INT,
    emp_nationality_idfk INT,
    emp_work_status_idfk INT,
    emp_marital_status_idfk INT,
    emp_email VARCHAR(100),
    emp_phone_nos VARCHAR(20),
    emp_address_idfk INT,
    emp_loyalty_point INT,
    emp_job_title_idfk INT,
    emp_created_on DATETIME,
    emp_edited_on DATETIME,
    emp_created_by_user_idfk VARCHAR(10),
    emp_edited_by_user_idfk VARCHAR(10)
);

-- Create Users Table
CREATE TABLE tbl_users_086 (
    usr_idpk INT IDENTITY(1,1) PRIMARY KEY,
    usr_username VARCHAR(50) NOT NULL UNIQUE,
    usr_password VARCHAR(256) NOT NULL,
    usr_empidfk INT REFERENCES tbl_employees_086(emp_idpk),
    usr_roleidfk INT REFERENCES tbl_user_roles_086(role_id),
    usr_start_date DATETIME,
    usr_end_date DATETIME,
    usr_created_by_userid INT,
    usr_edited_by_userid INT,
    usr_created_on DATETIME,
    usr_edited_on DATETIME
);

-- Create Customers Table
CREATE TABLE tbl_customers_086 (
    cus_id INT IDENTITY(1,1) PRIMARY KEY,
    cus_firstname VARCHAR(15) NOT NULL,
    cus_lastname VARCHAR(15) NOT NULL,
    cus_othernames VARCHAR(50) NOT NULL,
    cus_dob DATE NOT NULL,
    cus_gender_idfk INT,
    cus_nationality_idfk INT,
    cus_marital_status_idfk INT,
    cus_occupation VARCHAR(30),
    cus_email VARCHAR(100) NOT NULL,
    cus_phone_nos VARCHAR(20),
    cus_address TEXT NOT NULL,
    cus_loyalty_points INT,
    cus_created_on DATETIME,
    cus_edited_on DATETIME,
    cus_created_by_user_idfk VARCHAR(10),
    cus_edited_by_user_idfk VARCHAR(10)
);

-- Create Account Details Table
CREATE TABLE tbl_account_details_086 (
    acc_account_number INT IDENTITY(1,1) PRIMARY KEY,
    acc_customer_id INT NOT NULL,
    acc_account_type VARCHAR(20),
    acc_balance DECIMAL(15, 2) NOT NULL
);

-- Create KYC Table
CREATE TABLE tbl_kyc_086 (
    kyc_id INT IDENTITY(1,1) PRIMARY KEY,
    kyc_customer_id INT NOT NULL UNIQUE,
    kyc_id_type VARCHAR(20),
    kyc_id_number VARCHAR(50) NOT NULL UNIQUE,
    kyc_document_url VARCHAR(255),
    kyc_verified_by INT,
    kyc_verified_at DATETIME
);

-- Create Transactions Table
CREATE TABLE tbl_transactions_086 (
    tst_transaction_id INT IDENTITY(1,1) PRIMARY KEY,
    tst_account_number INT NOT NULL,
    tst_amount DECIMAL(15, 2) NOT NULL,
    tst_transaction_type VARCHAR(20),
    tst_created_by_user_id INT,
    tst_created_on DATETIME
);
