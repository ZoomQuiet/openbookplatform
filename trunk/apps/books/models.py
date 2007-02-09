from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import dispatcher

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
    
class CommentInfo(models.Model):
    chapter = models.ForeignKey(Chapter)
    comment_num = models.CharField(maxlength=20)
    count = models.IntegerField(default=0)

C_STATUS = ((0, 'None'), (1, 'Good'), (2, 'Bad'))
class Comment(models.Model):
    chapter = models.ForeignKey(Chapter)
    comment_num = models.CharField(maxlength=20)
    username = models.CharField(maxlength=50)
    email = models.EmailField()
    website = models.URLField(default='')
    content = models.TextField()
    status = models.IntegerField(choices=C_STATUS, default=0)
    replay = models.TextField(default='')
    createtime = models.DateTimeField(auto_now_add=True)
    
    class Admin:pass
    
    class Meta:
        ordering = ['createtime']
        
    def __str__(self):
        return self.content
    
def pre_save_comment(sender, instance, signal, *args, **kwargs):
    if instance.id == None:
        try:
            info = CommentInfo.objects.get(chapter=instance.chapter, comment_num=instance.comment_num)
        except CommentInfo.DoesNotExist:
            info = CommentInfo.objects.create(chapter=instance.chapter, comment_num=instance.comment_num)
        info.count += 1
        info.save()

def post_delete_comment(sender, instance, signal, *args, **kwargs):
    if instance.id == None:
        try:
            info = CommentInfo.objects.get(chapter=instance.chapter, comment_num=instance.comment_num)
        except CommentInfo.DoesNotExist:
            return
        
        if info.count <= 1:
            info.delete()
        else:
            info.count -= 1
            info.save()

dispatcher.connect(pre_save_comment , signal=signals.pre_save, sender=Comment)
dispatcher.connect(post_delete_comment , signal=signals.post_delete, sender=Comment)
