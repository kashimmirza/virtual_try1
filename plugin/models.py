# myapp/models.py
from django.db import models


class Customer(models.Model):
    image = models.ImageField(upload_to='customers/')
    body_measurements = models.JSONField()


class Clothing(models.Model):
    measurements = models.JSONField()
