from django.db import models
from django.contrib.auth.models import User
from .utils import *

# Create your models here.

class ItemsTracked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=220, blank=True)
    url = models.URLField()
    current_price = models.FloatField(blank=True)
    old_price = models.FloatField(default=0)
    price_difference = models.FloatField(default=0)
    desired_price = models.FloatField(default=0)
    website = models.CharField(max_length=50)
    status = models.BooleanField(default = False)

    def __str__(self):
        return "%s" % (self.name)

    def save(self, *args, **kwargs):
        name, price = GetData(self.url, self.website)
        old_price = self.current_price
        if self.current_price:
            if price != old_price:
                diff = price - old_price
                self.price_difference = round(diff, 2)
                self.old_price = old_price
            else:
                self.old_price = 0
                self.price_difference = 0

        self.name = name
        self.current_price = price

        super().save(*args, **kwargs)
