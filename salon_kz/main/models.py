from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser
from main.constants import USER_TYPES, CLIENT, ORDER_FLAGS, NEW_ORDER
from datetime import datetime
from django.contrib.postgres.fields import ArrayField

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

class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
    
    def __str__(self):
        return self.name
    

class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
    
    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client')    

    def __str__(self):
        return self.user.__str__()
    

class Partner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='partner')

    def __str__(self):
        return self.user.__str__()

class Salon(models.Model):
    name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=12,null=True)
    address = models.CharField( max_length=250, default=None, null=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='salons')
    is_aproved = models.BooleanField(default=False)
    card_number = models.CharField(max_length=16)
    work_start = models.TimeField(auto_now_add=True)
    work_end = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='salon_services')

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.name

class Master(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='master')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='masters', null=True, blank=True)
    is_aproved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.__str__()


class MasterService(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='service_masters')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='master_services')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='salon_master_services', null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    date_time_created = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=datetime.today)
    time = models.TimeField()
    master_service = models.ForeignKey(MasterService, on_delete=models.CASCADE, related_name='order_price')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_orders')
    flag = models.CharField(choices=ORDER_FLAGS, default=NEW_ORDER, max_length=50)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='partner_orders')

    def __str__(self):
        return self.master_service.__str__()

class Comment(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment_owners')

    text = models.TextField()
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='salon_comments')

    def __str__(self):
        return self.text


class Rating(models.Model):
    rate = models.IntegerField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rating_owners')

    def __str__(self):
        return  self.owner.__str__ + str(self.rate)

class ClientRating(Rating):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_ratings')

    def __str__(self):
        return super().__str__()

class SalonRating(Rating):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='salon_ratings')

    def __str__(self):
        return super().__str__()

class MasterRating(Rating):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='master_ratings')

    def __str__(self):
        return super().__str__()