# from typing_extensions import Required
from django.db import models
# from django.creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user( 
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=25)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(verbose_name="username", max_length=30, unique=True, primary_key=True)
    # password = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Resturants(models.Model):
    #h_id,h_name,owner ,location,rooms
    name = models.CharField(max_length=30,default="French Peran")
    owner = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50,default="Texas")
    country = models.CharField(max_length=50,default="USA")
    def __str__(self):
        return self.name


class Tables(models.Model):
    Table_STATUS = ( 
    ("1", "available"), 
    ("2", "not available"),    
    ) 

    Table_TYPE = ( 
    ("1", "Large Table"), 
    ("2", "Medium Table"),
    ("3","Couple Tables"),    
    ) 

    #type,no_of_rooms,capacity,prices,Hotel
    table_type = models.CharField(max_length=50,choices = Table_TYPE)
    capacity = models.IntegerField()
    price = models.IntegerField()
    size = models.IntegerField()
    Resturants = models.ForeignKey(Resturants, on_delete = models.CASCADE)
    status = models.CharField(choices =Table_STATUS,max_length = 15)
    table_number = models.IntegerField(auto_created=True)
    def __str__(self):
        return self.Resturants.name


# class Payment(models.Model):
#     cc_number = CardNumberField(_('card number'))
#     cc_expiry = CardExpiryField(_('expiration date'))
#     cc_code = SecurityCodeField(_('security code'))
    
class Reservation(models.Model):
    name = models.CharField(max_length=50)
    # lname = models.CharField(max_length=25)
    phone = models.CharField(max_length=10, null=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    partysize = models.IntegerField()
    date_joined = models.DateTimeField(auto_now=True)
    arrival = models.DateTimeField()
    reservation_fee = models.IntegerField(default=10)
    # check_out = models.DateField()
    card_no = models.IntegerField(max_length=16 )
    expiration = models.CharField(max_length=6  )
    cvc = models.IntegerField(max_length=3)

    Table = models.ForeignKey(Tables, on_delete = models.CASCADE)
    members =models.BooleanField(default=False)
    user = models.ForeignKey(Account,  primary_key=True, default=None, on_delete= models.CASCADE)
    

    def __str__(self):
        return self.user.username


