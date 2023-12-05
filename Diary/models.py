from django.db import models
from Authentication.models import User



class Diary(models.Model):
    title = models.CharField(max_length=80, unique=True)
    content = models.CharField(max_length=8096)
    mood_score = models.IntegerField(default=0)
    sleep_score = models.IntegerField(default=0)
    eat_score = models.IntegerField(default=0) 
    create_time = models.DateField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    class Meta: 
        ordering = ['-create_time']

class Image(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    image = models.ImageField('images', upload_to='diary', null=True)


