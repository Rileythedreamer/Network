from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    content = models.CharField(max_length=600)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    
    def calculate_likes(self):
        self.likes = Like.objects.filter(liked=self).count()
        return self.likes
    

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name = "following" , on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name= "followed_by" , on_delete=models.CASCADE)

    class Meta:
        unique_together = ("follower", "followed")
        
class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('liker', 'liked')