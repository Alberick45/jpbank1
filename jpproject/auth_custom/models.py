from django.db import models

# Create your models here.


class TblUsers086(models.Model):
    usr_idpk = models.AutoField(primary_key=True)
    usr_username = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    usr_password = models.CharField(max_length=256, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    usr_empidfk = models.IntegerField(blank=True, null=True)
    usr_start_date = models.DateTimeField(blank=True, null=True)
    usr_end_date = models.DateTimeField(blank=True, null=True)
    usr_created_by_userid = models.IntegerField(blank=True, null=True)
    usr_edited_by_userid = models.IntegerField(blank=True, null=True)
    usr_created_on = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    usr_edited_on = models.DateTimeField(blank=True, null=True,auto_now=True)

    class Meta:
        db_table = 'tbl_users_086'

class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    sht_name = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_user_roles_086"  # Matches your table name

    def __str__(self):
        return self.name
