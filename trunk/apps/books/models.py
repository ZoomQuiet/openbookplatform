from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(maxlength=100)
    description = models.TextField()
    author = models.ManyToManyField(User, related_name = "author")
    createdate = models.DateTimeField(auto_now_add=True)
    modifydate = models.DateTimeField(auto_now=True)
    icon = models.ImageField(upload_to="books_icon", blank=True, null=True)
    
    class Admin:pass
    
    class Meta:
        ordering = ['-modifydate']
        
    def __str__(self):
        return self.title
    
class Chapter(models.Model):
    book = models.ForeignKey(Book)
    num = models.CharField(maxlength=20, unique=True)
    title = models.CharField(maxlength=100)
    abstract = models.TextField()
    modifydate = models.DateTimeField(auto_now=True)
    content = models.TextField()
    
    class Admin:pass
    
    class Meta:
        ordering = ['num']
        
    def __str__(self):
        return self.title
    
