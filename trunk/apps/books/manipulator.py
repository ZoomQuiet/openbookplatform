from apps.easyform import EasyManipulator
from apps.books.models import Comment, Chapter

class AddCommentManipulator(EasyManipulator):
    def __init__(self, request, chapter_num):
        self.request = request
        self.chapter_num = chapter_num
        fields = [
            dict(type='TextField', field_name="username", is_required=True),
            dict(type='EmailField', field_name="email", length=28, maxlength=30, is_required=True),
            dict(type='URLField', field_name="website", is_required=False),
            dict(type='LargeTextField', field_name="content", is_required=True),
        ]
        self.init(fields)

    def save(self, data):
        chapter = Chapter.objects.get(num=self.chapter_num)
        
        if data['website']:
            website = data['website']
        else:
            website = ''
        obj = Comment.objects.create(chapter=chapter, comment_num=data['comment_num'],
            username=data['username'], email=data['email'], website=website,
            content=data['content'])
        
        return obj
    
