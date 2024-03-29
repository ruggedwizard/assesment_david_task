from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    CHOICES = (
        ('todo','todo'),
        ('in progress','in progress'),
        ('completed','completed')
    )
    title = models.CharField(null=True,blank=True,max_length=255)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(null=True, blank=True, default=False)
    status = models.CharField(max_length=255, null=True, blank=True, choices = CHOICES, default ='todo')
    created_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return str(self.title)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length =255, null=True, blank=True)
    last_name = models.CharField(max_length =255, null=True, blank=True)
    phone = models.CharField(max_length = 255, null=True, blank=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name) + 'Profile'
