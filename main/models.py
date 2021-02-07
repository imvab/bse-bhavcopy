from django.db import models

# Create your models here.


class Stock(models.Model):
    code = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    open = models.CharField(max_length=200)
    high = models.CharField(max_length=200)
    low = models.CharField(max_length=200)
    close = models.CharField(max_length=200)

    def __str__(self):
        return self.name
