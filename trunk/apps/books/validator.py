from apps.books.models import Comment, Chapter, Book
import utils.validator as valid
from django.contrib.auth.models import User

class AddCommentValidator(valid.Validator):
    username = valid.CharField()
    email = valid.EmailField(max_length=30)
    website = valid.URLField(required=False, default='')
    content = valid.CharField()
    comment_num = valid.CharField()
    
    def __init__(self, request, book_id, chapter_num):
        self.request = request
        self.chapter_num = chapter_num
        self.book_id = book_id

    def save(self, data):
        book = Book.objects.get(pk=int(self.book_id))
        chapter = Chapter.objects.get(num=self.chapter_num, book=book)
        
        obj = Comment.objects.create(book=book, chapter=chapter, comment_num=data['comment_num'],
            username=data['username'], email=data['email'], website=data['website'],
            content=data['content'])
        
        return obj
    
class BookValidator(valid.Validator):
    title = valid.CharField()
    description = valid.CharField()
    license = valid.CharField(required=False, default='')
    icon = valid.CharField(required=False)
    
    def __init__(self, request, object_id=None):
        self.object_id = object_id
        self.request = request
        
    def save(self, data):
        if not self.object_id:
            obj = Book.objects.create(title=data['title'], description=data['description'], license=data['license'])
            obj.authors.add(self.request.user)
        else:
            obj = Book.objects.get(pk=int(self.object_id))
            obj.title = data['title']
            obj.description = data['description']
            obj.license = data['license']
            obj.save()
            
        if data['icon']:
            from utils import image, fileutil
        
            filename = 'book_' + str(obj.id) + '.jpg'
            filename = fileutil.resetfilename(filename, 'books_icon')
            obj.save_icon_file(filename, image.thumbnail_string(data['icon']['content'], size=(70,93)))
    
        return obj
 

class ChapterValidator(valid.Validator):
    title = valid.CharField()
    abstract = valid.CharField(required=False, default='')
    content = valid.CharField()
    num = valid.CharField()
    
    def __init__(self, request, book_id, object_id=None):
        self.object_id = object_id
        self.book_id = book_id
        self.book = Book.objects.get(pk=int(book_id))
        self.request = request
        self.fields['num'].add_validator(self.isValidNum)
    
    def isValidNum(self, field_data, all_data):
        if not self.object_id:
            try:
                Chapter.objects.get(num=field_data, book=self.book)
            except Chapter.DoesNotExist:
                return
            else:
                raise valid.ValidationError, _("This chapter num has been used.")
    
    def save(self, data):
        if not self.object_id:
            obj = Chapter.objects.create(title=data['title'], abstract=data['abstract'],
                content=data['content'], num=data['num'], book=self.book)
        else:
            obj = Chapter.objects.get(pk=int(self.object_id))
            obj.title = data['title']
            obj.content = data['content']
            obj.num = data['num']
            obj.abstract = data.get('abstract', '')
            obj.save()
            
        return obj
    
class AddUserValidator(valid.Validator):
    username = valid.CharField()
    
    def __init__(self, book_id):
        self.book_id = book_id
        self.fields['username'].add_validator(self.IsValidUser)
    
    def IsValidUser(self, data, all_data):
        try:
            user = User.objects.get(username=data)
        except User.DoesNotExist:
            raise valid.ValidationError, _("User %s don't exist." % data)
        
    def save(self, data):
        user = User.objects.get(username=data['username'])
        book = Book.objects.get(pk=int(self.book_id))
        for u in book.authors.all():
            if u.username == data['username']:
                break
        else:
            book.authors.add(user)
            
        return user
        