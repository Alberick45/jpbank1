# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TblAccountDetails086(models.Model):
    acc_account_number = models.AutoField()
    acc_customer_id = models.IntegerField()
    acc_account_type = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    acc_balance = models.DecimalField(max_digits=15, decimal_places=2)
    acc_status = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    acc_account_pin = models.IntegerField()
    acc_created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_account_details_086'


class TblAddress086(models.Model):
    adr_address_idpk = models.AutoField()
    adr_address = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_address_086'


class TblCountry086(models.Model):
    cty_idpk = models.AutoField()
    cty_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cty_shortname = models.CharField(max_length=6, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cty_nationality = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cty_created_by_user_idfk = models.IntegerField(blank=True, null=True)
    cty_edited_by_user_idfk = models.IntegerField(blank=True, null=True)
    cty_created_on = models.DateTimeField(blank=True, null=True)
    cty_edited_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_country_086'


class TblCustomers086(models.Model):
    cus_id = models.AutoField(primary_key=True)
    cus_firstname = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')
    cus_lastname = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')
    cus_othernames = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    cus_dob = models.DateField()
    cus_gender_idfk = models.IntegerField(blank=True, null=True)
    cus_nationality_idfk = models.IntegerField(blank=True, null=True)
    cus_marital_status_idfk = models.IntegerField(blank=True, null=True)
    cus_occupation = models.CharField(max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cus_email = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    cus_phone_nos = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cus_address = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')  # This field type is a guess.
    cus_loyalty_points = models.IntegerField(blank=True, null=True)
    cus_created_on = models.DateTimeField(blank=True, null=True)
    cus_edited_on = models.DateTimeField(blank=True, null=True)
    cus_created_by_user_idfk = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cus_edited_by_user_idfk = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_customers_086'


class TblEmployees086(models.Model):
    emp_idpk = models.AutoField()
    emp_firstname = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')
    emp_lastname = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    emp_othernames = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    emp_dob = models.DateField()
    emp_gender_idfk = models.IntegerField(blank=True, null=True)
    emp_nationality_idfk = models.IntegerField(blank=True, null=True)
    emp_work_status_idfk = models.IntegerField(blank=True, null=True)
    emp_marital_status_idfk = models.IntegerField(blank=True, null=True)
    emp_email = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    emp_phone_nos = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    emp_address_idfk = models.IntegerField(blank=True, null=True)
    emp_loyalty_point = models.IntegerField(blank=True, null=True)
    emp_job_title_idfk = models.IntegerField(blank=True, null=True)
    emp_created_on = models.DateTimeField(blank=True, null=True)
    emp_edited_on = models.DateTimeField(blank=True, null=True)
    emp_created_by_user_idfk = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    emp_edited_by_user_idfk = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_employees_086'


class TblGender086(models.Model):
    gnd_gender_idpk = models.AutoField()
    gnd_geder_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_gender_086'


class TblKyc086(models.Model):
    kyc_id = models.AutoField(primary_key=True)
    kyc_customer_id = models.IntegerField(unique=True)
    kyc_id_type = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    kyc_id_number = models.CharField(unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    kyc_document_url = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    kyc_verified_by = models.IntegerField(blank=True, null=True)
    kyc_verified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_kyc_086'


class TblMaritalStatus086(models.Model):
    mts_marital_status_idpk = models.AutoField()
    mts_marital_status_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_marital_status_086'


class TblSecurityLogs086(models.Model):
    log_id = models.AutoField()
    log_customer_account_number = models.IntegerField(blank=True, null=True)
    log_employee_id = models.IntegerField()
    log_action = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    log_ip_address = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    log_device_info = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    log_timestamp = models.DateTimeField(blank=True, null=True)
    success = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_security_logs_086'


class TblTransactions086(models.Model):
    tst_transaction_id = models.AutoField()
    tst_account_number = models.IntegerField()
    tst_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tst_transaction_type = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tst_created_by_user_id = models.IntegerField(blank=True, null=True)
    tst_created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_transactions_086'


class TblUserRoles086(models.Model):
    name = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    sht_name = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    edited_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_user_roles_086'


class TblUsers086(models.Model):
    usr_idpk = models.AutoField()
    usr_username = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    usr_password = models.CharField(max_length=256, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    usr_empidfk = models.IntegerField(blank=True, null=True)
    usr_start_date = models.DateTimeField(blank=True, null=True)
    usr_end_date = models.DateTimeField(blank=True, null=True)
    usr_created_by_userid = models.IntegerField(blank=True, null=True)
    usr_edited_by_userid = models.IntegerField(blank=True, null=True)
    usr_created_on = models.DateTimeField(blank=True, null=True)
    usr_edited_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_users_086'
