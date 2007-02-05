#coding=utf-8
from django.utils.translation import gettext_lazy as _
from apps.easyform import EasyManipulator
from django.db.models import ObjectDoesNotExist
from models import Group
from django.core import validators
from django.contrib.auth.models import User

from PIL import Image
import StringIO

class UserRegisterManipulator(EasyManipulator):
    def __init__(self, request):
        self.request = request
        self.object_id = None
        fields = [
            dict(type='TextField', verbose_name=_('Username:'), field_name="username", length=28, maxlength=30, is_required=True,
                validator_list=[self.isValidUser]),
            dict(type='PasswordField', verbose_name=_('Password:'), field_name="password", length=15, maxlength=30, is_required=True,
                validator_list=[validators.AlwaysMatchesOtherField('password1', _("Please enter the password")), self.isValidPassword]),
            dict(type='PasswordField', verbose_name=_('Confirm password:'), field_name="password1", length=15, maxlength=30, is_required=True),
            dict(type='EmailField', verbose_name=_('Email Address:'), field_name="email", length=28, maxlength=30, is_required=True,
                validator_list=[self.isValidEmail]),
        ]
        self.init(fields)

    def isValidUser(self, field_data, all_data):
        if not field_data:
            raise validators.ValidationError, _("Username cann't be empty.")
    
        if len(field_data) < 4:
            raise validators.ValidationError, _("The length of username cann't be less then 4.")
    
        for c in field_data:
            if c in '~`!@#$%^&*();:\'",./<>?\|+= ':
                raise validators.ValidationError, _("There cannot be invalidate character in user name")

        if not self.object_id:
            try:
                User.objects.get(username=field_data)
            except ObjectDoesNotExist:
                return
            else:
                raise validators.ValidationError, _("The username has been registered, please try another one.")
    
    def isValidPassword(self, field_data, all_data):

        if len(field_data) < 4:
            raise validators.ValidationError, _("For your account security, please don't use the password which length is less than 4.")

    def isValidEmail(self, field_data, all_data):
        if not field_data:
            raise validators.ValidationError, "Email cann't be empty."
        try:
            validators.isValidEmail(field_data, None)
        except validators.ValidationError:
            raise validators.ValidationError,  "This email has been used."

        if not self.object_id:
            try:
                User.objects.get(email=field_data)
            except ObjectDoesNotExist:
                return
            else:
                raise validators.ValidationError, "This email has been used."

    def save(self, new_data):
        u = User.objects.create_user(new_data["username"], new_data["email"], new_data["password"])
        u.is_staff = True
        u.is_active = True
        u.is_superuser = False
        u.save()
        return u

class UserEditManipulator(UserRegisterManipulator):
    def __init__(self, request, object_id):
        self.request = request
        self.object_id = object_id
        fields = [
            dict(type='PasswordField', verbose_name=_('Password:'), field_name="password", length=15, maxlength=30,
                validator_list=[validators.AlwaysMatchesOtherField('password1', _("Please enter the password")), self.isValidPassword]),
            dict(type='PasswordField', verbose_name=_('Confirm password:'), field_name="password1", length=15, maxlength=30),
            dict(type='EmailField', verbose_name=_('Email Address:'), field_name="email", length=28, maxlength=30, is_required=True),
        ]
        self.init(fields)

    def isValidPassword(self, field_data, all_data):
        if 0 < len(field_data) < 4:
            raise validators.ValidationError, _("For your account security, please don't use the password which length is less than 4.")
    
    def save(self, new_data):
        u = User.objects.get(pk=int(self.object_id))
        u.email = new_data['email']
        if new_data.get('password', ''):
            u.set_password(new_data['password'])
        u.save()
        
        return u
    
def isValidSize(field_data, all_data):
    im = Image.open(StringIO.StringIO(field_data["content"]))
    if im.size[0] > 150 or im.size[1] > 150:
        raise validators.ValidationError, "The image size should be in 150 * 150"

class UserPortraitManipulator(EasyManipulator):
    def __init__(self, request, user):
        self.request = request
        self.user = user
        fields = [
#            dict(type='ImageUploadField', verbose_name=_("Your portrait:"), field_name="portrait", validator_list=[isValidSize]),
            dict(type='ImageUploadField', verbose_name=_("Your portrait:"), field_name="portrait"),
        ]
        self.init(fields)
    
    def save(self, data=None):
        if data.get('portrait', None):
            user = self.user
            from utils import image, fileutil
        
            filename = 'users_' + user.username + '.jpg'
            filename = fileutil.resetfilename(filename, 'photo')
            user.userprofile.save_portrait_file(filename, image.thumbnail_string(data['portrait']['content']))

        return self.user
    
class AdminGroupManipulator(EasyManipulator):
    def __init__(self, user, object_id=None):
        self.user = user
        self.object_id = object_id
        fields = [
            dict(type='TextField', verbose_name='小组名称', field_name="name", length=30, maxlength=100, is_required=True),
            dict(type='FileUploadField', verbose_name='小组图标', field_name="icon"),
            dict(type='LargeTextField', verbose_name='小组说明', rows=3, cols=60, field_name="description"),
            dict(type='TextField', verbose_name='管理员', field_name="managers", length=30, maxlength=100),
        ]
                
        self.init(fields)

    def save(self, data):
        if not self.object_id:
            obj = Group.objects.create(name=data['name'], description=data.get('description', ''))
        else:
            obj = Group.objects.get(pk=int(self.object_id))
            obj.name = data['name']
            obj.description = data.get('description', '')
            obj.save()
            
        if data.get('icon', ''):
            from utils import image, fileutil

            #get gbk filename
            filename = 'groups_' + str(obj.id) + '.jpg'
            filename = fileutil.resetfilename(filename, 'groups')
            obj.save_icon_file(filename, image.thumbnail_string(data['icon']['content']))
            obj.save()

        names = data.get('managers', '').split()
        obj.managers.clear()
        for m in names:
            try:
                o = User.objects.get(username=m)
            except User.DoesNotExist:
                continue
            obj.managers.add(o)
            
        return obj

