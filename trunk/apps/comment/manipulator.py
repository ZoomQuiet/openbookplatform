#coding=utf-8
from apps.easyform import EasyManipulator
from apps.comment.models import Comment

class EasyCommentManipulator(EasyManipulator):
    def __init__(self, user, content_object=None, owner_object=None, object_id=None):
        self.user = user
        self.object_id = object_id
        self.content_object = content_object
        self.owner_object = owner_object
        fields = [
            dict(type='LargeTextField', verbose_name='回复内容', rows=6, cols=50, field_name="content", is_required=True),
        ]
                
        self.init(fields)
    
    def save(self, data):
        if self.object_id:
            obj = Comment.objects.get(pk=int(self.object_id))
            obj.content = data['content']
            obj.save()
        else:
            obj = Comment.objects.create(content_object=self.content_object, content=data['content'], user=self.user, owner_object=self.owner_object)
        return obj
