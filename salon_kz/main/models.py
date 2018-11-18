from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser
from main.constants import USER_TYPES, CLIENT, ORDER_FLAGS, NEW_ORDER, TIMES
from datetime import datetime

class CustomUserManager(BaseUserManager):

    def create_user(self, username, password=None, is_active=None, user_type='client'):
        if not username:
            raise ValueError('User must have a username')
        user = self.model(username=username, user_type=user_type)
        user.set_password(password)
        if is_active is not None:
            user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):

        user = self.create_user(username, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def for_user(self, user):
        return self.filter(user=user)

    def get_masters(self, master_name):
        users = self.filter(user_type='master').filter(first_name__contains=master_name)
        masters = [user.master for user in users]
        return masters



class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=50, null=False, db_index=True, verbose_name='Username', unique=True)
    telephone = models.CharField(max_length=12, null=True, db_index=True, verbose_name='Telephone', unique=True)
    first_name = models.CharField(max_length=50, null=True, verbose_name='First name', blank=True)
    last_name = models.CharField(max_length=50, null=True, verbose_name='Last name', blank=True)
    email = models.EmailField(null=True)

    user_type = models.CharField(max_length=20, choices=USER_TYPES, null=True, blank=True, default=CLIENT)


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name="Admin")

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []


    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username
    