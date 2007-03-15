#Validator
#============
#
#This module is not aimed to replace the newforms, but I would like manually write html code,
#and just need a pure validate module, so I write this, and many things may be similar with
#newforms. So if you like me would only need a pure validator module, you can use it.
#
#And it has some different features from newforms:
#    
#1. Support validator_list parameter, so you could use it just like the old manipuator class
#2. Supply easy method, such as `validate_and_save()`, so you can pass a request object, and 
#   get a tuple result `(flag, obj_or_error)`, if the `flag` is `True`, then the next value 
#   is an object; and if the `flag` is `False`, then the next value is error message.
#3. Each field has a `validate_and_get` method, and it'll validate first and then return the 
#   result, maybe an object or error message. Just like above.
#4. SplitDateTimeField is somewhat different from the newforms. For example::
#    
#    c = SplitDateTimeField('date', 'time')
#    print c.validate_and_get({'date':'2006/11/30', 'time':'12:13'})
#
#    So the first parameter is DateField's field_name, and the second parameter is TimeField's
#    field_name.
#5. Add yyyy/mm/dd date format support
#6. Support default value of a field. You can add a default value for a field, if this field 
#   is not required, and the value is *empty*, Validator will return the default value.
#    
#This module is new, so many things could be changed.
#
#Version: 0.5
#Author: limodou<limodou AT gmail.com>
#Update:
#    * 2007/02/17 0.1
#    * 2007/02/26 0.2 Fixed add_validator bug
#    * 2007/03/04 0.3 Add COOKIES and GET support, so the validate data will come 
#                     from GET, POST, COOKIES, FILES
#    * 2007/03/06 0.4 Add FileField, ImageField support
#    * 2007/03/14 0.5 Add model support


import datetime
import time
import re
import copy
from django.utils.datastructures import MultiValueDict
from django.utils.datastructures import SortedDict
from django.core import validators

__all__ = (
    'Field', 'CharField', 'IntegerField',
    'DEFAULT_DATE_INPUT_FORMATS', 'DateField',
    'DEFAULT_TIME_INPUT_FORMATS', 'TimeField',
    'DEFAULT_DATETIME_INPUT_FORMATS', 'DateTimeField',
    'RegexField', 'EmailField', 'URLField', 'BooleanField',
    'ComboField', 'SplitDateTimeField', 'FileField',
    'ImageField',
    'ValidationError', 'Validator',
    'isChoices', 'isMultipleChoices',
)

try:
    set
except:
    from sets import Set as set
    
from django.utils.translation import gettext as _
#def _(v):
#    return v

class SortedDictFromList(SortedDict):
    "A dictionary that keeps its keys in the order in which they're inserted."
    # This is different than django.utils.datastructures.SortedDict, because
    # this takes a list/tuple as the argument to __init__().
    def __init__(self, data=None):
        if data is None: data = []
        self.keyOrder = [d[0] for d in data]
        dict.__init__(self, dict(data))

    def copy(self):
        l = []
        for k, v in self.items():
            l.append((k, copy.copy(v)))
            v.validator_list = copy.copy(v.validator_list)
        return SortedDictFromList(l)

class ValidationError(Exception):
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return str(self.message)

class Field(object):
    
    creation_counter = 0
    
    def __init__(self, field_name=None, required=True, multi_value=False, default=None, validator_list=None):
        self.field_name = field_name
        self.required = required
        self.default = default
        self.multi_value = multi_value
        self.default_validator_list = []
        if validator_list:
            self.validator_list = validator_list
        else:
            self.validator_list = []
            
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1
        
    def __str__(self):
        return '<%s:field_name=%r,required=%r,default=%s\nvalidator_list=%r>' % (self.__class__.__name__, self.field_name, self.required, self.default, self.validator_list)
            
    def get_data_from_datadict(self, all_data):
        if not self.multi_value or not isinstance(all_data, MultiValueDict):
            return all_data.get(self.field_name, None)
        else:
            return all_data.getlist(self.field_name)
        
    def validate_and_get(self, data, all_data=None):
        if not data:
            if not self.required:
                if self.default is not None:
                    return True, self.default
                else:
                    return True, None
            else:
                return False, _(u'This field is required.')
        try:
            if isinstance(data, list):
                v = []
                for i in data:
                    v.append(self.convert(i, all_data))
                data = v
            else:
                data = self.convert(data, all_data)
        except ValidationError, e:
            return False, e.message
        except:
            return False, _(u'Convert data error.')
        try:
            for v in self.default_validator_list + self.validator_list:
                v(data, all_data)
        except ValidationError, e:
            return False, e.message
        except validators.ValidationError, e:
            return False, e.messages[0]
        return True, data
                
    def convert(self, data, all_data=None):
        raise Exception, 'Not implement yet!'
    
    def add_validator(self, validator):
        if isinstance(validator, (list, tuple)):
            self.validator_list.extend(validator)
        else:
            self.validator_list.append(validator)
    
class ValidatorMetaclass(type):
    """
    Metaclass that converts Field attributes to a dictionary called
    """
    def __new__(cls, name, bases, attrs):
        fields = []
        removed_fields = attrs.get('__removed_fields__', [])
        has_fields = attrs.get('__has_fields__', [])
        model = attrs.get('__model__', None)
        if model:
            opts = model._meta
            for f in opts.fields:
                if f.name not in removed_fields and ((has_fields and f.name in has_fields) or not has_fields):
                    p = convert_model_field(f)
                    if p:
                        #print '-------------', p, p.field_name
                        fields.append((p.field_name, p))
        else:
            attrs['__model__'] = None
                    
        for field_name, obj in attrs.items():
            if isinstance(obj, Field) and field_name not in removed_fields:
                obj = attrs.pop(field_name)
                obj.field_name = field_name
                fields.append((field_name, obj))
        fields.sort(lambda x, y: cmp(x[1].creation_counter, y[1].creation_counter))

        for base in bases[::-1]:
            if hasattr(base, 'base_fields'):
                fields = base.base_fields.items() + fields

        attrs['base_fields'] = SortedDictFromList(fields)
        
        old_init = attrs.get('__init__', None)
        def _f(self, *args, **kwargs):
            self.fields = self.base_fields.copy()
            self._clean_data = None
            if old_init:
                old_init(self, *args, **kwargs)
        attrs['__init__'] = _f
                
        return type.__new__(cls, name, bases, attrs)
    
class Validator(object):
    
    __metaclass__ = ValidatorMetaclass
    
    def validate(self, request_or_data):
        all_data = MultiValueDict()
        if hasattr(request_or_data, 'COOKIES'):
            all_data.update(request_or_data.COOKIES.copy())
        if hasattr(request_or_data, 'GET'):
            all_data.update(request_or_data.GET.copy())
        if hasattr(request_or_data, 'POST'):
            all_data.update(request_or_data.POST.copy())
            all_data.update(request_or_data.FILES.copy())
        else:
            all_data = request_or_data
        if all_data:
            errors = {}
            new_data = {}
            
            #gather all fields
            for field_name, field in self.fields.items():
                new_data[field_name] = field.get_data_from_datadict(all_data)
            
            #validate and gather the result
            result = {}
            for field_name, field in self.fields.items():
                flag, value = field.validate_and_get(new_data[field_name], new_data)
                if not flag:
                    if isinstance(value, dict):
                        errors.update(value)
                    else:
                        errors[field_name] = value
                else:
                    result[field_name] = value
                    
            if flag:
                #validate global        
                try:
                    self.full_validate(result, new_data)
                except ValidationError, e:
                    errors['_'] = e.message
            
            #if there is errors, then result (False, error_messages)
            if errors or not flag:
                return False, errors
            
            self._clean_data = result
            return True, result
            
        else:
            return False, {'_':_(u'There is not data posted.')}
        
    def validate_and_save(self, request):
        flag, result = self.validate(request)
        if flag:
            #then try do the save
            try:
                obj = self.save(result)
            except:
                import traceback
                traceback.print_exc()
                return False, {'_':_(u'Saving object error.')}
            
            return True, obj
        else:
            return flag, result
        
    def _get_clean_data(self):
        if self._clean_data is None:
            raise Exception, _('Validate method has not been executed!')
        return self._clean_data

    def save(self, data):
        return self.default_save(data)
        
    def default_save(self, data):
        if self.__model__:
            params = {}
            for f in self.__model__._meta.fields:
                v = data.get(f.name, None)
                if v is not None:
                    params[f.name] = v
            
            return self.__model__._default_manager.create(**params)
        raise ValidationError, _('Cannot find the __model__ attribute.')
        
    def default_update(self, data, object_id_or_instance):
        if self.__model__:
            if not isinstance(object_id_or_instance, self.__model__):
                _id = int(object_id_or_instance)
                obj = self.__model__._default_manager.get(id=_id)
            else:
                obj = object_id_or_instance
            for f in self.__model__._meta.fields:
                v = data.get(f.name, None)
                if v is not None:
                    setattr(obj, f.name, v)
            obj.save()
            return obj
        raise ValidationError, _('Cannot find the __model__ attribute.')
    
    def full_validate(self, new_data, all_data):
        pass

class CharField(Field):
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
        self.max_length, self.min_length = max_length, min_length
        self.default_validator_list.append(self.validate_length)
        
    def validate_length(self, data, all_data=None):
        if self.max_length is not None and len(data) > self.max_length:
            raise ValidationError, _(u'Ensure this value has at most %d characters.') % self.max_length
        if self.min_length is not None and len(data) < self.min_length:
            raise ValidationError, _(u'Ensure this value has at least %d characters.') % self.min_length
        
    def convert(self, data, all_data=None):
        return str(data)
    
class IntegerField(Field):
    def __init__(self, max_value=None, min_value=None, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)
        self.max_value, self.min_value = max_value, min_value
        self.default_validator_list.append(self.validate_value)
        
    def validate_value(self, data, all_data=None):
        if self.max_value is not None and data > self.max_value:
            raise ValidationError, _(u'Ensure this value is less than or equal to %s.') % self.max_value
        if self.min_value is not None and data < self.min_value:
            raise ValidationError, _(u'Ensure this value is greater than or equal to %s.') % self.min_value
      
    def convert(self, data, all_data=None):
        try:
            return int(data)
        except (ValueError, TypeError):
            raise ValidationError, _(u'Enter a whole number.')

DEFAULT_DATE_INPUT_FORMATS = (
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%Y/%m/%d',  # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
)

class DateField(Field):
    def __init__(self, input_formats=None, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)
        self.input_formats = input_formats or DEFAULT_DATE_INPUT_FORMATS
        
    def convert(self, data, all_data=None):
        for format in self.input_formats:
            try:
                return datetime.date(*time.strptime(data, format)[:3])
            except ValueError:
                continue
        raise ValidationError, _(u'Date format is not right.')

DEFAULT_TIME_INPUT_FORMATS = (
    '%H:%M:%S',     # '14:30:59'
    '%H:%M',        # '14:30'
)

class TimeField(Field):
    def __init__(self, input_formats=None, *args, **kwargs):
        super(TimeField, self).__init__(*args, **kwargs)
        self.input_formats = input_formats or DEFAULT_TIME_INPUT_FORMATS
        
    def convert(self, data, all_data=None):
        for format in self.input_formats:
            try:
                return datetime.time(*time.strptime(data, format)[3:6])
            except ValueError:
                continue
        raise ValidationError, _(u'Time format is not right.')

DEFAULT_DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%Y/%m/%d %H:%M:%S',     # '2006/10/25 14:30:59'
    '%Y/%m/%d %H:%M',        # '2006/10/25 14:30'
    '%Y/%m/%d ',             # '2006/10/25 '
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
)

class DateTimeField(Field):
    def __init__(self, input_formats=None, *args, **kwargs):
        super(DateTimeField, self).__init__(*args, **kwargs)
        self.input_formats = input_formats or DEFAULT_DATETIME_INPUT_FORMATS
        
    def convert(self, data, all_data=None):
        for format in self.input_formats:
            try:
                return datetime.datetime(*time.strptime(data, format)[:6])
            except ValueError:
                continue
        raise ValidationError, _(u'Time format is not right.')

class RegexField(CharField):
    def __init__(self, regex, error_message=None, *args, **kwargs):
        super(RegexField, self).__init__(*args, **kwargs)
        if isinstance(regex, basestring):
            regex = re.compile(regex)
        self.regex = regex
        self.default_validator_list.append(self.validate_string)
        self.error_message = error_message or _(u'Enter a valid value.')
        
    def validate_string(self, data, all_data=None):
        if not self.regex.match(data):
            raise ValidationError, self.error_message

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain

class EmailField(RegexField):
    def __init__(self, *args, **kwargs):
        super(EmailField, self).__init__(email_re, _(u'Enter a valid e-mail address.'), *args, **kwargs)
        
url_re = re.compile(
    r'^https?://' # http:// or https://
    r'(?:[A-Z0-9-]+\.)+[A-Z]{2,6}' # domain
    r'(?::\d+)?' # optional port
    r'(?:/?|/\S+)$', re.IGNORECASE)

class URLField(RegexField):
    def __init__(self, verify_exists=False, validator_user_agent='User Agent', *args, **kwargs):
        super(URLField, self).__init__(url_re, _(u'Enter a valid URL.'), *args, **kwargs)
        self.verify_exists = verify_exists
        self.user_agent = validator_user_agent
        self.default_validator_list.append(self.validate_url)

    def validate_url(self, data, all_data=None):
        if self.verify_exists:
            import urllib2
            headers = {
                "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
                "Accept-Language": "en-us,en;q=0.5",
                "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                "Connection": "close",
                "User-Agent": self.user_agent,
            }
            try:
                req = urllib2.Request(data, None, headers)
                u = urllib2.urlopen(req)
            except ValueError:
                raise ValidationError, _(u'Enter a valid URL.')
            except: # urllib2.URLError, httplib.InvalidURL, etc.
                raise ValidationError, _(u'This URL appears to be a broken link.')
        return data
    
class BooleanField(Field):
    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(*args, **kwargs)
        
    def convert(self, data, all_data=None):
        if isinstance(data, basestring):
            if data.lower() in ('on', 'true', 'yes', 'ok'):
                return True
            elif data.lower() in ('off', 'false', 'no', 'cancel'):
                return False
            else:
                raise ValidationError, _(u'Need a boolean value.')
        else:
            try:
                return bool(data)
            except:
                raise ValidationError, _(u'Need a boolean value.')
            
class ComboField(Field):
    def __init__(self, fields=(), *args, **kwargs):
        super(ComboField, self).__init__(*args, **kwargs)
        self.fields = fields

    def get_data_from_datadict(self, all_data):
        data = {}
        for field in self.fields:
            data[field.field_name] = field.get_data_from_datadict(all_data)
        return data
            
    def validate_and_get(self, data, all_data=None):
        errors = {}
        result = {}
        for field in self.fields:
            flag, value = field.validate_and_get(data[field.field_name], data)
            if not flag:
                if isinstance(value, dict):
                    errors.update(value)
                else:
                    errors[field.field_name] = value
            else:
                result[field.field_name] = value
        
        if not errors or not flag:
            try:
                data = self.convert(result, all_data)
            except ValidationError, e:
                return False, e.message
            except:
                return False, _(u'Convert data error.')
            
        return True, data
                
    def convert(self, data, all_data=None):
        raise Exception, 'Not implement yet!'
    
class SplitDateTimeField(ComboField):
    def __init__(self, date_field, time_field, field_name=None, *args, **kwargs):
        '''
        field_name should be (date_fieldname, time_fieldname)
        '''
        self.date_fieldname = date_field
        self.time_fieldname = time_field
        fields = [DateField(field_name=self.date_fieldname, *args, **kwargs), TimeField(field_name=self.time_fieldname, *args, **kwargs)]
        super(SplitDateTimeField, self).__init__(fields, field_name=field_name, *args, **kwargs)
        
    def convert(self, data, all_data=None):
        try:
            return datetime.datetime.combine(data[self.date_fieldname], data[self.time_fieldname])
        except:
            raise ValidationError, _(u'Time format is not right.')
        
class FileField(Field):
    def __init__(self, filesize=None, *args, **kwargs):
        super(FileField, self).__init__(*args, **kwargs)
        self.filesize = filesize
        self.default_validator_list.append(self.validate_filesize)
        
    def convert(self, data, all_data=None):
        return data
    
    def validate_filesize(self, data, all_data=None):
        if self.filesize and len(data['content']) > self.filesize:
            raise ValidationError, _(u'Filesize is exceeded the limit %d.') % self.filesize
        
class ImageField(FileField):
    def __init__(self, filesize=None, *args, **kwargs):
        super(ImageField, self).__init__(filesize, *args, **kwargs)
        self.default_validator_list.append(validators.isValidImage)
        
def _get_choices_keys(choices):
    if isinstance(choices, dict):
        keys = set(choices.keys())
    elif isinstance(choices, (list, tuple)):
        keys = set([])
        for v in choices:
            if isinstance(v, (list, tuple)):
                keys.add(v[0])
            else:
                keys.add(v)
    else:
        raise ValidationError, _(u'Choices need a dict, tuple or list data.')
    return keys

def isChoices(choices):
    '''
    choices should be a list or a tuple, e.g. [1,2,3]
    '''
    def _f(data, all_data=None):
        if data not in _get_choices_keys(choices):
            raise ValidationError, _(u'Select a valid choice. That choice is not one of the available choices.')
    return _f

def isMultipleChoices(choices):
    '''
    choices should be a list or a tuple, e.g. [1,2,3]
    '''
    def _f(data, all_data=None):
        data = set(data)
        if data - _get_choices_keys(choices):
            raise ValidationError, _(u'Select a valid choice. That choice is not one of the available choices.')
    return _f
            
from django.db import models

fields_mapping = [
    (BooleanField, models.BooleanField),
    (CharField, (models.CharField, models.FilePathField, models.IPAddressField, models.PhoneNumberField, models.SlugField, models.TextField, models.USStateField, models.XMLField)),
    (DateField, models.DateField),
    (EmailField, models.EmailField),
    (FileField, models.FileField),
    (ImageField, models.ImageField),
    (IntegerField, (models.IntegerField, models.OrderingField, models.PositiveIntegerField, models.SmallIntegerField, models.PositiveSmallIntegerField)),
    (SplitDateTimeField, models.DateTimeField),
    (TimeField, models.TimeField),
    (URLField, models.URLField),
]
def convert_model_field(field):
    flag = False
    fk = None
    if field.__class__.__name__ == 'AutoField':
        return
    
    kwargs = {'field_name':field.name}
    fieldclass = field.__class__.__name__
    for f, fields in fields_mapping:
        if isinstance(fields, (list, tuple)):
            for i in fields:
                if i.__name__ == fieldclass:
                    flag = True
                    break
        else:
            if fields.__name__ == fieldclass:
                flag = True
        if flag:
            fk = f
            #for now editable only used for date* field
            if not field.editable:
                return
            if field.blank:
                kwargs['required'] = False
            if field.default is not models.NOT_PROVIDED:
                kwargs['default'] = field.default
            break
    if fk in [BooleanField, DateField, EmailField, FileField, ImageField, IntegerField, TimeField, URLField]:
        return fk(**kwargs)
    elif fk in [CharField]:
        kwargs['max_length'] = field.maxlength
        return fk(**kwargs)
    elif fk in [SplitDateTimeField]:
        return fk(field.name + '_date', field.name + '_time', **kwargs)
    else:
        print 'Cannot find a match field', field
                    
if __name__ == '__main__':
    c = CharField()
    print c.validate_and_get('abc')
    print c.validate_and_get('')
    print c.validate_and_get(None)
    c = CharField(max_length=10)
    print c.validate_and_get('abcdefghijklmn')
    c = CharField(required=False)
    print c.validate_and_get('')
    print c.validate_and_get('abc')
    c = IntegerField()
    print c.validate_and_get('abc')
    print c.validate_and_get('123')
    print c.validate_and_get(123)
    c = DateField()
    print c.validate_and_get('abc')
    print c.validate_and_get('2007/02/16')
    c = TimeField()
    print c.validate_and_get('abc')
    print c.validate_and_get('01:22:34')
    print c.validate_and_get('01:22')
    c = DateTimeField()
    print c.validate_and_get('abc')
    print c.validate_and_get('2007/02/13 01:22:34')
    print c.validate_and_get('2006-01-01 01:22')
    c = RegexField('\d+')
    print c.validate_and_get('abc')
    print c.validate_and_get('123')
    c = EmailField()
    print c.validate_and_get('abc')
    print c.validate_and_get('abc@gmail.com')
    c = URLField()
    print c.validate_and_get('abc')
    print c.validate_and_get('http://sina.com.cn')
    c = BooleanField()
    print c.validate_and_get('abc')
    print c.validate_and_get('True')
    c = IntegerField(validator_list=[isChoices([1,2,3])])
    print c.validate_and_get('a')
    print c.validate_and_get('1')
    print c.validate_and_get('4')
    c = IntegerField(validator_list=[isMultipleChoices([1,2,3])])
    print c.validate_and_get(['a'])
    print c.validate_and_get(['1', '2'])
    print c.validate_and_get(['1', '4'])
    c = SplitDateTimeField('date', 'time')
    print c.validate_and_get({'date':'2006/11/30', 'time':'12:13'})
    
    data = {'username':'limodou', 'email':'abc@gmail.com', 'age':'123', 'password':'limodou'}
    
    def validate_username(data, all_data):
        print 'validate_username', data
        if data != 'limodou':
            raise ValidationError, 'Username must be "limodou"'
    
    class TV(Validator):
        username = CharField(validator_list=[validate_username])
        email = EmailField()
        age = IntegerField()
        password = CharField()
        __removed_fields__ = ['age']
        
        def __init__(self):
            self.fields['username'].add_validator(self.AnotherValidator)
        
        def full_validate(self, data, all_data):
            if not data.has_key('password'):
                raise ValidationError, _(u'Need password')
            
        def save(self, data):
            print 'ok'
            
        def AnotherValidator(self, data, all_data):
            print 'AnotherValidator', data
            return
        
    t = TV()
    print t.fields
    print t.validate_and_save(data)
    t = TV()
    print t.validate_and_save(data)
    
    from django.contrib.auth.models import User
    class TV1(Validator):
        __model__ = User
        
    t = TV1()
    for f, o in t.fields.items():
        print f, o
    
    
    