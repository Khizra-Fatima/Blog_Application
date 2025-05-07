from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import math 


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name



class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    content = models.TextField(blank=False, null=False)
    short_description = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(blank=True)
    publish_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured_image = models.ImageField(default='blog_feature_images/default_featured_img.png', upload_to='blog_feature_images/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def estimate_read_time(self):
        words_per_minute = 200
        word_count = len(self.content.split())  #count words in content
        return math.ceil(word_count / words_per_minute)  #round up time
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} Created by {self.author}, related to {self.category} category'



















class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.SmallIntegerField(choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog')  #ensures a user can only like/dislike a blog once
        indexes = [
            models.Index(fields=['user', 'blog']),  #optimized queries
        ]

    def __str__(self):
        return f"{self.user} - {'Like' if self.reaction == 1 else 'Dislike'} on {self.blog.title}"
    


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'
    




