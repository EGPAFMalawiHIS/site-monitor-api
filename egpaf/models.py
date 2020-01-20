

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class User_Manager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an username')
        user = self.model(email=email,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email, password=password,)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password,)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=60, blank=False, null=False)
    last_name = models.CharField(max_length=60, blank=False, null=False)
    image_url = models.CharField(max_length=60, blank=True, null=True)
    username = models.CharField(max_length=60, blank=False, unique=False)
    email = models.EmailField(
                verbose_name='email address', max_length=60,
                blank=True, unique=True)
    phone = models.CharField(
                verbose_name='phone number', max_length=60,
                blank=True, unique=False)
    active = models.BooleanField(default=False)
    # Admin user; non super-user
    staff = models.BooleanField(default=False)
    # Superuser
    admin = models.BooleanField(default=False)
    # verification_code = models.CharField(
    #                         max_length=10, blank=False, null=False)
    # expiration_time = models.DateTimeField(blank=True, null=True)
    is_verified = models.PositiveSmallIntegerField(default=0)
    # Notice the absence of a "Password field", that's built in.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = User_Manager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active

    class Meta:
        managed = True
        db_table = 'users'

class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)

    class Meta:
        managed = True
        db_table = 'districts'

class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=60, unique=True)
    district_id = models.ForeignKey('District', models.DO_NOTHING)
    longitude = models.CharField(max_length=60)
    latitude = models.CharField(max_length=60)

    class Meta:
        managed = True
        db_table = 'sites'


class Monitor(models.Model):
    monitor_id = models.AutoField(primary_key=True, unique=True)
    status = models.IntegerField(blank=True, null=True)
    sitecode = models.ForeignKey(Site, related_name='site', to_field="code", db_column="sitecode", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'monitors'

