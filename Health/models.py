from datetime import date
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Medicine(models.Model):
    name = models.CharField(max_length=80, unique=True)
    note = models.CharField(max_length=2048, default='')
    amount = models.CharField(max_length=256)
    select_time = models.CharField(max_length=1024)
    unit = models.CharField(max_length=64, default='单位')
    start_date = models.DateField()
    finish_date = models.DateField()
    create_time = models.DateTimeField(auto_now_add=True)

    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
