from django.db.models import Model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from authentication.manager import CustomUserManager
from datetime import datetime, timedelta
import jwt
from backend import settings

# Create your models here.

ADMIN = 1; MENTOR= 2;USER = 3

USER_TYPE = (
    (ADMIN, 'Admin'),
    (MENTOR, 'Mentor'),
    (USER, 'User'),
)

username_regex = RegexValidator(regex=r'^[a-z\d\_]+$',message="Enter only lower case letter and '_' and Alphanumeric. Upper case letter not Allow", )
email_regex = RegexValidator(regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',message="Enter valid email address")
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+91'. Up to 13 digits allowed.")

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True,validators=[username_regex],max_length=30, null=False, blank=False)
    email = models.EmailField(unique=True,validators=[email_regex],max_length=30)
    phone = models.CharField(unique=True,validators=[phone_regex], max_length=20, blank=True, null=True)
    # PERMITION_FIELD = 'role'
    role = models.PositiveSmallIntegerField(choices=USER_TYPE, default=3)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    # Event Time
    created_on = models.DateTimeField(auto_now_add =True)
    created_by = models.CharField(max_length=30)
    modified_on = models.DateTimeField(auto_now =True)
    modified_by =  models.CharField(max_length=30)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
