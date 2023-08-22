# goats_app/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)

        # print('email is',email)
        # print('pass is',password)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    SELLER = 'Seller'
    AGENT = 'Agent'
    BUYER = 'Buyer'
    TYPE_CHOICES = [
        (SELLER, 'Seller'),
        (AGENT, 'Agent'),
        (BUYER, 'Buyer'),
    ]
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # Use email as the username
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'type']

    def __str__(self):
        return self.name

class Goat(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    SEX_CHOICES = [(MALE, 'Male'), (FEMALE, 'Female')]
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    weight = models.FloatField()
    load = models.ForeignKey('Load', on_delete=models.CASCADE, related_name='goats', null=True, blank=True)
    sales = models.ForeignKey('Sales', on_delete=models.CASCADE, related_name='goats', null=True, blank=True)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goats_as_seller')
    buyer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goats_as_buyer', null=True, blank=True)


class Load(models.Model):
    master = models.ForeignKey('Load', on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loads')
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loads_as_seller',null=True, blank=True)
    paid_amount = models.FloatField()
    due_amount = models.FloatField()

class Sales(models.Model):
    amount_paid = models.FloatField()
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_as_agent')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_as_buyer')
