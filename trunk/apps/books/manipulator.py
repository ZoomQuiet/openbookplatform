from apps.easyform import EasyManipulator
from apps.books.models import Comment, Chapter, Book
from django.core import validators

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
    
class BookManipulator(EasyManipulator):
    def __init__(self, request, object_id=None):
        self.object_id = object_id
        self.request = request
        fields = [
            dict(type='TextField', field_name="title", is_required=True),
            dict(type='LargeTextField', field_name="description", is_required=True),
            dict(type='ImageUploadField', field_name="icon", is_required=False),
        ]
        self.init(fields)
        
    def save(self, data):
        if not self.object_id:
            obj = Book.objects.create(title=data['title'], description=data['description'])
            obj.authors.add(self.request.user)
        else:
            obj = Book.objects.get(pk=int(self.object_id))
            obj.title = data['title']
            obj.description = data['description']
            obj.save()
            
        if data.get('icon', None):
            from utils import image, fileutil
        
            filename = 'book_' + obj.id + '.jpg'
            filename = fileutil.resetfilename(filename, 'books_icon')
            obj.save_icon_file(filename, image.thumbnail_string(data['icon']['content'], size=(70,93)))
    
        return obj
    
class ChapterManipulator(EasyManipulator):
    def __init__(self, request, book_id, object_id=None):
        self.object_id = object_id
        self.book_id = book_id
        self.book = Book.objects.get(pk=int(book_id))
        self.request = request
        fields = [
            dict(type='TextField', field_name="title", is_required=True),
            dict(type='LargeTextField', field_name="abstract", is_required=False),
            dict(type='LargeTextField', field_name="content", is_required=True),
            dict(type='TextField', field_name="num", is_required=True, 
                validator_list=[self.isValidNum]),
        ]
        self.init(fields)
        
    def isValidNum(self, field_data, all_data):
        if not field_data:
            raise validators.ValidationError, "Chapter num cann't be empty."
        if not self.object_id:
            try:
                Chapter.objects.get(num=field_data, book=self.book)
            except Chapter.DoesNotExist:
                return
            else:
                raise validators.ValidationError, "This chapter num has been used."
    
    def save(self, data):
        if not self.object_id:
            obj = Chapter.objects.create(title=data['title'], abstract=data.get('abstract', ''),
                content=data['content'], num=data['num'], book=self.book)
        else:
            obj = Chapter.objects.get(pk=int(self.object_id))
            obj.title = data['title']
            obj.content = data['content']
            obj.num = data['num']
            obj.abstract = data.get('abstract', '')
            obj.save()
            
        return obj
    
