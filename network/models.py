from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    content = models.TextField(blank=False)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.content}'
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes')
    reaction = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post')
        ]