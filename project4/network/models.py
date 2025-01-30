from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

  
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}."
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author.username} : {self.content[:30]}"
  
class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts_liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.liker} liked {self.post} at {self.timestamp}."
 