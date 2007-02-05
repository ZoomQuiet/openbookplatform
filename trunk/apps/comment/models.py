#coding=utf-8
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import dispatcher
from datetime import datetime

class CommentInfo(models.Model):
    lastreplytime = models.DateTimeField(auto_now=True)    #最后回复时间
    lastresponser = models.ForeignKey(User, related_name='lastresponser')     #最后回复人
    count = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    scorecount = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = models.GenericForeignKey()
    
    def __str__(self):
        return 
    
    def get_score(self):
        return self.score / self.scorecount
    
class Comment(models.Model):
    commentinfo = models.ForeignKey(CommentInfo)
    title = models.CharField(default='', maxlength=200)
    content = models.TextField(default='')
    createtime = models.DateTimeField(auto_now_add=True)
    modifytime = models.DateTimeField(auto_now=True, db_index=True)
    user = models.ForeignKey(User)
    score = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, related_name='target')
    object_id = models.IntegerField()
    content_object = models.GenericForeignKey()
    owner_type = models.ForeignKey(ContentType, related_name='owner')
    owner_id = models.IntegerField()
    owner_object = models.GenericForeignKey(ct_field='owner_type', fk_field='owner_id')
    
    def __str__(self):
        return self.title
    
    class Admin:pass
    
    class Meta:
        ordering = ['createtime']
        
def pre_save_comment(sender, instance, signal, *args, **kwargs):
    if instance.id == None:
        ctype = ContentType.objects.get_for_model(instance.content_object)
        try:
            info = CommentInfo.objects.get(content_type__pk=ctype.id, object_id=instance.object_id)
        except CommentInfo.DoesNotExist:
            info = CommentInfo.objects.create(lastresponser=instance.user, content_object=instance.content_object)
        instance.commentinfo = info
        info.count += 1
        if instance.score > 0:
            info.scorecount += 1
            info.score += instance.score
        info.lastresponser = instance.user
        info.lastreplytime = datetime.now()
        info.save()

def post_delete_comment(sender, instance, signal, *args, **kwargs):
    if instance.id == None:
        info = instance.commentinfo
        if info.count <= 1:
            info.delete()
        else:
            info.count -= 1
            if info.score > 0:
                info.scorecount -= 1
                info.score -= instance.score
            info.save()

dispatcher.connect(pre_save_comment , signal=signals.pre_save, sender=Comment)
dispatcher.connect(post_delete_comment , signal=signals.post_delete, sender=Comment)
