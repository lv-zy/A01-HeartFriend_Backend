from django.db import models

# Create your models here.


class counter(models.Model): 
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)