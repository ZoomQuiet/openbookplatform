from utils import validator as valid
from django.core import validators
from django.contrib.auth.models import User

class LoginValidator(valid.Validator):
    username = valid.CharField()
    password = valid.CharField()
    
class RegisterValidator(valid.Validator):
    username = valid.CharField(max_length=30, min_length=4)
    password = valid.CharField(max_length=30, min_length=4, validator_list=[validators.AlwaysMatchesOtherField('password1', _("Please enter the password"))])
    password1 = valid.CharField(max_length=30)
    email = valid.EmailField(max_length=30)
    
    def __init__(self, request):
        self.fields['username'].add_validator(self.isValidUser)
        self.fields['password'].add_validator(self.isValidPassword)
        self.fields['email'].add_validator(self.isValidEmail)

    def isValidUser(self, field_data, all_data):
        for c in field_data:
            if c in '~`!@#$%^&*();:\'",./<>?\|+= ':
                raise valid.ValidationError, _("There cannot be invalidate character in user name")

        try:
            User.objects.get(username=field_data)
        except User.DoesNotExist:
            return
        else:
            raise valid.ValidationError, _("The username has been registered, please try another one.")
    
    def isValidPassword(self, field_data, all_data):
        if len(field_data) < 4:
            raise valid.ValidationError, _("For your account security, please don't use the password which length is less than 4.")

    def isValidEmail(self, field_data, all_data):
        try:
            validators.isValidEmail(field_data, None)
        except validators.ValidationError:
            raise valid.ValidationError,  "This email has been used."

        try:
            User.objects.get(email=field_data)
        except User.DoesNotExist:
            return
        else:
            raise valid.ValidationError, "This email has been used."

    def save(self, data):
        u = User.objects.create_user(data["username"], data["email"], data["password"])
        u.is_staff = True
        u.is_active = True
        u.is_superuser = False
        u.save()
        return u

class ChangeValidator(RegisterValidator):
    portrait = valid.ImageField(required=False)
    
    def __init__(self, request, user_id):
        self.user_id = user_id
        del self.fields['username']
        self.fields['password'].required = False
        self.fields['password1'].required = False
   
    def save(self, data):
        u = User.objects.get(pk=int(self.user_id))
        u.email = data['email']
        if data.get('password', ''):
            u.set_password(data['password'])
        u.save()
        
        if data.get('portrait', None):
            from utils import image, fileutil
        
            filename = 'users_' + u.username + '.jpg'
            filename = fileutil.resetfilename(filename, 'photo')
            u.get_profile().save_portrait_file(filename, image.thumbnail_string(data['portrait']['content']))
        
        return u
    