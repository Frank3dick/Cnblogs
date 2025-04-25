from django.db import models

from accounts.models import User
from categories.models import Category


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    summary = models.TextField()
    author_id = models.ForeignKey(User, to_field='id',on_delete=models.CASCADE, related_name='articles')
    category_id = models.ForeignKey(Category, to_field='id',on_delete=models.CASCADE, related_name='articles')
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.title