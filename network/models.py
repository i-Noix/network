from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    content = models.TextField(blank=False)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.content}'