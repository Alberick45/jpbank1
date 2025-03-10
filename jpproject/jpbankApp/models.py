# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove ` managed = False  # Add this` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        db_table = 'auth_group'  # Proper indentation

class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, on_delete=models.DO_NOTHING)  # Added on_delete
    permission = models.ForeignKey('AuthPermission', on_delete=models.DO_NOTHING)  # Added on_delete

    class Meta:
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)



from django.db import models

class CoreUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_customer = models.BooleanField(default=False)  # Added default <button class="citation-flag" data-index="4">
    is_admin = models.BooleanField(default=False)    # Added default <button class="citation-flag" data-index="4">

    class Meta:
        db_table = 'core_user'
        # managed = False  # Removed per <button class="citation-flag" data-index="6"> and <button class="citation-flag" data-index="9">

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        db_table = 'auth_group'
        # managed = False  # Removed per <button class="citation-flag" data-index="6"> and <button class="citation-flag" data-index="9">

class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(
        AuthGroup, 
        on_delete=models.CASCADE,  # Added per <button class="citation-flag" data-index="7">
        related_name='group_permissions'  # Added per <button class="citation-flag" data-index="5">
    )
    permission = models.ForeignKey(
        'AuthPermission', 
        on_delete=models.CASCADE,  # Added per <button class="citation-flag" data-index="7">
        related_name='group_permissions'  # Added per <button class="citation-flag" data-index="5">
    )

    class Meta:
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)
        # managed = False  # Removed per <button class="citation-flag" data-index="6"> and <button class="citation-flag" data-index="9">

class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(
        'DjangoContentType', 
        on_delete=models.CASCADE,  # Added per <button class="citation-flag" data-index="7">
        related_name='content_type_permissions'  # Added per <button class="citation-flag" data-index="5">
    )
    codename = models.CharField(max_length=100)

    class Meta:
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)
        # managed = False  # Removed per <button class="citation-flag" data-index="6"> and <button class="citation-flag" data-index="9">

class CoreUserGroups(models.Model):
    user = models.ForeignKey(
        CoreUser, 
        on_delete=models.CASCADE,  # Added per <button class="citation-flag" data-index="7">
        related_name='user_groups'  # Added per <button class="citation-flag" data-index="5">
    )
    group = models.ForeignKey(
        AuthGroup, 
        on_delete=models.CASCADE,  # Added per <button class="citation-flag" data-index="7">
        related_name='user_groups'  # Added per <button class="citation-flag" data-index="5">
    )

    class Meta:
        db_table = 'core_user_groups'
        unique_together = (('user', 'group'),)
        # managed = False  # Removed per <button class="citation-flag" data-index="6"> and <button class="citation-flag" data-index="9">

class CoreUserUserPermissions(models.Model):
    user = models.ForeignKey(
        CoreUser, 
        on_delete=models.CASCADE,  # Added per <button class="citation-flag" data-index="7">
        related_name='user_permissions'  # Added per <button class="citation-flag" data-index="5">
    )
    permission = models.ForeignKey(
        AuthPermission, 
        on_delete=models.CASCADE,  # Added per <button class="citation-flag" data-index="7">
        related_name='user_permissions'  # Added per <button class="citation-flag" data-index="5">
    )

    class Meta:
        db_table = 'core_user_user_permissions'
        unique_together = (('user', 'permission'),)
        # managed = False  # Removed per <button class="citation-flag" data-index="6"> and <button class="citation-flag" data-index="9">

class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)
        # managed = False  # Removed per <button class="citation-flag" data-index="6"> and <button class="citation-flag" data-index="9">

class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        db_table = 'django_migrations'
        # managed = False  # Removed per <button class="citation-flag" data-index="6"> and <button class="citation-flag" data-index="9">

class TblAccountDetails086(models.Model):
    acc_account_number = models.CharField(primary_key=True, max_length=20)
    acc_customer = models.ForeignKey(
        CoreUser, 
        on_delete=models.CASCADE,  # Added per <button class="citation-flag" data-index="7">
        db_column='acc_customer_id',  # Preserved existing column <button class="citation-flag" data-index="8">
        related_name='accounts'  # Added per <button class="citation-flag" data-index="5">
    )
    acc_balance = models.DecimalField(max_digits=10, decimal_places=2)
    acc_type = models.CharField(max_length=50)
    acc_created_at = models.DateTimeField()

    class Meta:
        db_table = 'tbl_account_details_086'
        # managed = False  # Removed per <button class="citation-flag" data-index="6"> and <button class="citation-flag" data-index="9">

class TblKyc086(models.Model):
    kyc_id = models.AutoField(primary_key=True)
    kyc_customer = models.ForeignKey(
        CoreUser, 
        on_delete=models.CASCADE,  # Added per <button class="citation-flag" data-index="7">
        db_column='kyc_customer_id',  # Preserved existing column <button class="citation-flag" data-index="8">
        related_name='kyc_records'  # Added per <button class="citation-flag" data-index="5">
    )
    kyc_document_type = models.CharField(max_length=50)
    kyc_document_number = models.CharField(max_length=50)
    kyc_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_kyc_086'
        # managed = False  # Removed per <button class="citation-flag" data-index="6"> and <button class="citation-flag" data-index="9">



class TblMaritalStatus086(models.Model):
    mts_marital_status_idpk = models.AutoField()
    mts_marital_status_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
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
        db_table = 'tbl_security_logs_086'


class TblTransactions086(models.Model):
    tst_transaction_id = models.AutoField()
    tst_account_number = models.IntegerField()
    tst_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tst_transaction_type = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tst_created_by_user_id = models.IntegerField(blank=True, null=True)
    tst_created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_transactions_086'


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
        db_table = 'tbl_users_086'
