from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    image=models.ImageField(upload_to="profile_images", blank=True, null=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=100, null=True)
    bio=models.TextField()
    date=models.DateField(auto_now_add=True)
    followers=models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    def __str__(self):
        return self.username

    def total_followers(self):
        return self.followers.count()

    def total_following(self):
        return self.following.count()


class Blog(models.Model):
    image=models.ImageField(upload_to="blog_images")
    title=models.CharField(max_length=100)
    desc=models.TextField()
    tags=(
        ("Technology", "Technology"),
        ("Business", "Business"),
        ("Anime", "Anime"),
        ("Cars", "Cars"),
        ("Story", "Story"),
        ("Food", "Food"),
        ("Sports", "Sports"),
    )
    category=models.CharField(max_length=20, choices=tags, default="Technology")
    date=models.DateTimeField(auto_now_add=True, null=True)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    likes=models.ManyToManyField(User, related_name='blog_likes', blank=True)
    bookmarks=models.ManyToManyField(User, related_name='blog_bookmarks', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_bookmarks(self):
        return self.bookmarks.count()

class Review(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="Blog_reviews")
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    comment=models.TextField()