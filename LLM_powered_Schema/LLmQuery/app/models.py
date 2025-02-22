from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    supplier = models.CharField(max_length=255)
    store = models.CharField(max_length=255)
    price = models.IntegerField()
    discount_pcnt = models.IntegerField()


