from django.db import models

from accounts.models import User
from text_app.models import Article


# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    up_user_id = models.ForeignKey(User, to_field='id',on_delete=models.CASCADE, related_name='comments')
    article_id = models.ForeignKey(Article, to_field='id',on_delete=models.CASCADE, related_name='comments')
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['up_user_id', 'article_id']),
        ]
    def __str__(self):
        return self.id