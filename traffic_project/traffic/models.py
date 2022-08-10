from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Stream(models.Model):
    id = models.BigAutoField(db_column='ID',primary_key=True)
    message = models.CharField(max_length=100)

    def __str__(self):
        return self.message

    class Meta:
        managed = False
        db_table = 'stream'
    


class UserProfile(models.Model):
    user_account = models.CharField(db_column='USER_ACCOUNT', primary_key=True, max_length=16)  # Field name made lowercase.
    user_password = models.CharField(db_column='USER_PASSWORD', max_length=16)  # Field name made lowercase.
    user_nickname = models.CharField(db_column='USER_NICKNAME', max_length=20)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=450, db_collation='utf8_general_ci')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_profile'


class parking(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    tel = models.TextField(blank=True, null=True)
    servicetime = models.TextField(db_column='serviceTime', blank=True, null=True)  # Field name made lowercase.
    x = models.TextField(db_column='X', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '停車場'


class towing(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    tel = models.TextField(blank=True, null=True)
    servicetime = models.TextField(blank=True, null=True)
    x = models.TextField(db_column='X', blank=True, null=True)  # Field name made lowercase.
    y = models.TextField(db_column='Y', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '拖吊場'


class speedLot(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    function = models.TextField(blank=True, null=True)
    roadsection = models.TextField(blank=True, null=True)
    situation = models.TextField(blank=True, null=True)
    wxyz = models.TextField(blank=True, null=True)
    speedlimit = models.IntegerField(blank=True, null=True)
    x = models.TextField(db_column='X', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '測速桿'
