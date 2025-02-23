from django.db import models
from django.contrib.auth.models import AbstractUser

# User model with image field 
class User(AbstractUser):
    photo = models.ImageField(upload_to="users", default="users/default.jpg", blank=True, null=True)
    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"

# Model to manage Posts
class Blogs(models.Model):
    title=models.CharField(max_length=200)
    article=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    publish_date=models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.author}"
   