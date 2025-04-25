from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    create_time = models.DateField(auto_now_add=True, null=True)
    update_time = models.DateField(auto_now=True, null=True)
    def __str__(self):
        return self.username