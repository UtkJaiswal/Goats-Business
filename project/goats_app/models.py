# goats_app/models.py

from django.db import models

class User(models.Model):
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
