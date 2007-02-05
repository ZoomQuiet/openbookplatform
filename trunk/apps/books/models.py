from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(maxlength=100)
    description = models.TextField()
    author = models.ManyToManyField(User, related_name = "author")
    createdate = models.DateTimeField(auto_now_add=True)
    modifydate = models.DateTimeField(auto_now=True)
    
    class Admin:pass
    
    class Meta:
        ordering = ['-modifydate']
    
class Chapter(models.Model):
    num = models.CharField(maxlength=20)
    title = models.CharField(maxlength=100)
    abstract = models.TextField()
    modifydate = models.DateTimeField(auto_now=True)
    content = models.TextField()
    
    class Admin:pass
    
