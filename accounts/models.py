from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    image=models.ImageField(upload_to="profile_images" ,blank=True, null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    username=models.CharField(max_length=100,null=True)
    bio=models.TextField()
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.username

class Blog(models.Model):
    image=models.ImageField(upload_to="blog_images")
    title=models.CharField(max_length=100)
    desc=models.TextField()
    tags=(
        ("Technology","Technology"),
        ("Buisiness","Buisiness"),
        ("Anime","Anime"),
        ("Cars","Cars"),
        ("Story","Story"),
        ("Food","Food"),
        ("Sports","Sports"),
    )
    category=models.CharField(max_length=20,choices=tags,default="Technology")
    date=models.DateTimeField(auto_now_add=True,null=True)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.category

        