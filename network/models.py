from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class NPost_model(models.Model):
    post_content=models.CharField(max_length=150)
    users=models.ForeignKey(User, on_delete=models.CASCADE, related_name="posters")
    created=models.DateTimeField(auto_now_add=True)
    likes=models.IntegerField(default=0)
    user_likes=models.ManyToManyField(User,related_name="viewers_liked")

class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    followers=models.ManyToManyField(User,related_name="viewers")
    following=models.ManyToManyField(User,related_name="views")
    num_following=models.IntegerField(default=0)
    num_followers=models.IntegerField(default=0)

    