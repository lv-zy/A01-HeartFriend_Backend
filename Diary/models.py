from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Diary(models.Model):
    title = models.CharField(max_length=80)
    content = models.CharField(max_length=8096)
    mood_score = models.IntegerField(default=0)
    sleep_score = models.IntegerField(default=0)
    eat_score = models.IntegerField(default=0) 
    create_time = models.DateField(auto_now_add=True)
    images = models.CharField(max_length=4096, default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    class Meta: 
        ordering = ['-create_time']

class Image(models.Model):
    image = models.ImageField('image', upload_to='diary', null=True)


