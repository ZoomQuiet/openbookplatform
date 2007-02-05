from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template import loader, Context
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from utils.ajax import uni_str

class NoData(Exception):pass
SUCCESS = 1
FAIL = 2
NORMAL = 3

class FieldsCollection(object):
    default_data = {}
    def __init__(self, fields=[], extra_field_types={}):
        self.init(fields, extra_field_types)
        
    def add(self, field, verbose_name=None):
        self.fields.append(field)
        if verbose_name:
            field.verbose_name = verbose_name
        
    def init(self, fields, extra_field_types={}):
        self.fields = []
        for i in fields:
            t = i.pop('type')
            verbose_name = i.pop('verbose_name', '')
            if hasattr(forms, t):
                klass = getattr(forms, t)
            else:
                klass = extra_field_types[t]
            try:
                obj = klass(**i)
            except:
                print 'Error Class=', t
                raise
            i['type'] = t
            
            #add verbose_name to field object
            if verbose_name:
                i['verbose_name'] = verbose_name
                obj.verbose_name = verbose_name
            else:
                obj.verbose_name = ''
            if i.get('is_required', False):
                obj.label = '<label for="%s"><b>%s:</b></label>' % (i['field_name'], obj.verbose_name)
            else:
                obj.label = '<label for="%s">%s:</label>' % (i['field_name'], obj.verbose_name)
                        
            self.fields.append(obj)
            
######################### Widgets ######################

class Button(forms.FormField):
    def __init__(self, field_name, value=''):
        self.field_name = field_name
        self.value = value
        
    def __str__(self):
        return self.render()

    def render(self):
        return '<input id="%(id)s" name="%(name)s" value="%(value)s"/>' % {'id':self.get_id(), 
            'name':self.field_name, 'value':self.value}
            
class SubmitButton(Button):
    def render(self):
        return '<input id="%(id)s" type="submit" name="%(name)s" value="%(value)s"/>' % {'id':self.get_id(), 
            'name':self.field_name, 'value':self.value}

class FieldSet(FieldsCollection, forms.FormField):
    def __init__(self, title='', data=None, errors=None, fields=[], extra_field_types={}, template='easyform/fieldset.html'):
        self.title = title
        self.template = template
        self.data = data or {}
        self.errors = errors or {}
        self.init(fields, extra_field_types)
            
    def __str__(self):
        fieldset = forms.FormWrapper(self, self.data, self.errors)
        fieldset.title = self.title
        t = loader.get_template(self.template)
        c = {
            'fieldset': fieldset,
        }
        return t.render(Context(c))

######################### Action ########################
class Action:
    def __init__(self, name):
        self.name = name
        
    def __call__(self):
        pass
    
class TemplateAction(Action):
    def __call__(self, context):
        return render_to_response(self.name, context)
    
class RedirectAction(Action):
    def __call__(self, context=None):
        return HttpResponseRedirect(self.name)
    
######################### EasyForm #######################
def filter_empty(d):
    for k, v in d.items():
        if v is None:
            del d[k]
        else:
            if isinstance(v, dict):
                filter_empty(d[k])
                
def ajax_field(field, default_data):
    d = dict(zip(['label', 'name', 'value', 'options'], 
            [getattr(field, 'verbose_name', ''), field.field_name, default_data.get(field.field_name, ''), {'is_required':field.is_required}]))
    
    classname = field.__class__.__name__
    if classname in ('TextField', 'PasswordField', 'IntegerField', 
            'SmallIntegerField', 'PositiveIntegerField', 'PositiveSmallIntegerField', 
            'FloatField', 'DatetimeField', 'EmailField', 'URLField',
            'IPAddressField'):
        if classname in ('TextField', 'IntegerField', 'SmallIntegerField', 
                'PositiveIntegerField', 'PositiveSmallIntegerField', 'FloatField', 
                'DatetimeField', 'EmailField', 'URLField', 'IPAddressField'):
            input_type = 'text'
        else:
            input_type = 'password'
        options = {'length':field.length, 'maxlength':field.maxlength}
    elif classname == 'LargeTextField':
        input_type = 'textarea'
        options = {'rows':field.rows, 'cols':field.cols}
    elif classname == 'HiddenField':
        input_type = 'hidden'
    elif classname == 'CheckboxField':
        input_type = 'checkbox'
        options = {'checked':field.checked_by_default}
    elif classname == 'SelectField':
        input_type = 'select'
        options = {'options':field.choices, 'size':field.size}
    elif classname == 'SelectMultipleField':
        input_type = 'select'
        options = {'options':field.choices, 'size':field.size, 'multiple':'multiple'}
    elif classname == 'FileUploadField':
        input_type = 'file'
    elif classname == 'ImageUploadField':
        input_type = 'file'
    elif classname in ('DateField', 'TimeField', 'PhoneNumberField', 'USStateField'):
        input_type = 'text'
    else:
        raise Exception, 'Not support'
        
    d.update({'type':input_type})
    d["options"].update(options)
    filter_empty(d)
    return d

class EasyManipulator(FieldsCollection, forms.Manipulator):
    """An easy manipulator class
    fiedls = list of dict
    [dict(type='TextField', field_name="username", length=15, maxlength=30, is_required=True)]
    """
    def __init__(self, fields=[], default_data=None, extra_field_types={}, object_id=None):
        if default_data is not None:
            self.default_data = default_data
        else:
            self.default_data = {}
        self.object_id = object_id
        super(EasyManipulator, self).__init__(fields, extra_field_types)
        
    def save(self, data):
        """ should return the new oject"""
        pass
    
    def form(self, data={}, errors={}, **kwargs):
        form = forms.FormWrapper(self, data, errors)
        form.errors = [(x, self[x].verbose_name, ','.join([str(i) for i in y])) for x, y in errors.items()]
        return form

    def easyform(self, data=None, errors=None, buttons=[SubmitButton('submit', _('Save'))], **kwargs):
        if data is None and hasattr(self, 'default_data') and self.default_data:
            data = self.default_data
        form = EasyForm(self, data=data, errors=errors, buttons=buttons, **kwargs)
        return form
    
    def ajaxform(self):
        s = []
        for field in self.fields:
            s.append([ajax_field(field, self.default_data)])
        return simplejson.dumps(uni_str(s))

    def validate_and_save(self, request, post_bind=False):
        f, obj = self.validate(request, post_bind)
        if f:
            self.do_html2python(self.data)
            obj = self.save(self.data)
            
            return True, obj
        else:
            return f, obj
        
    def validate(self, request, post_bind=False):
        if request.GET and not post_bind:
            self.data = request.GET.copy()
        elif request.POST or request.FILES:
            self.data = request.POST.copy()
            if request.FILES:
                self.data.update(request.FILES)
        else:
            return False, {'_':_('No data')}
        self.prepare(self.data)
        self.errors = self.get_validation_errors(self.data)
        if not self.errors:
            return True, {}
        else:
            return False, self.errors

class EasyModelManipulator(EasyManipulator):
    def __init__(self, model, object_id=None, formfields=None):
        self.model = model
        self.opts = model._meta
        self.fields = []
        self.default_data = {}
        if formfields:
            self.formfields = formfields
        else:
            self.formfields = []
        self.object_id = object_id
        self.follow = self.opts.get_follow(None)
        self.display_fields = {}
        
        s = []
        for f in self.opts.fields + self.opts.many_to_many:
            if not self.formfields or f.name in self.formfields:
                if not self.formfields:
                    s.append(f.name)
                fs = f.get_manipulator_fields(self.opts, self, False)
                self.display_fields[f.name] = fs
                for i in fs:
                    i.verbose_name = f.verbose_name
                self.fields.extend(fs)
                d = f.get_default()
                if d is not None:
                    self.default_data[f.column] = d
        if not self.formfields:
            self.formfields = s
            
    def ajaxform(self):
        s = []
        for field in self.formfields:
            if self.display_fields[field]:
                s.append([ajax_field(f, self.default_data) for f in self.display_fields[field]])
        return simplejson.dumps(uni_str(s))
    
    def save(self, data):
        params = {}
        for key in data:
            for f in self.model._meta.fields:
                if key == f.column:
                    params[key] = data[key]

#        params = {}
#        for f in self.opts.fields:
#            # Fields with auto_now_add should keep their original value in the change stage.
#            auto_now_add =getattr(f, 'auto_now_add', False)
#            if not auto_now_add:
#                param = f.get_manipulator_new_data(data)
#            else:
#                param = f.get_default()
#            params[f.attname] = param
            
        if self.object_id is None:
            obj = self.model.objects.create(**params)
        else:
            obj = self.model.objects.get(pk=int(self.object_id))
            for key, value in params.items():
                if hasattr(obj, key):
                    setattr(obj, key, params[key])
            obj.save()
        # Now that the object's been saved, save any uploaded files.
        for f in self.opts.fields:
            if isinstance(f, models.FileField):
                f.save_file(data, obj, None, False, rel=False)

        # Save many-to-many objects. Example: Set sites for a poll.
        for f in self.opts.many_to_many:
            if self.follow.get(f.name, None):
                if not f.rel.edit_inline:
                    new_vals = data.getlist(f.name)
                    # First, clear the existing values.
                    rel_manager = getattr(obj, f.name)
                    rel_manager.clear()
                    # Then, set the new values.
                    for n in new_vals:
                        rel_manager.add(f.rel.to._default_manager.get(pk=n))
                    # TODO: Add to 'fields_changed'
        
        return obj
        
class EasyForm:
    def __init__(self, manipulator, form_template='', path='', data=None, errors=None, buttons=[], form_id=''):
        self.manipulator = manipulator
        self.type = type
        self.path = path
        self.buttons = buttons
        self.form_template = form_template
        self.form_id = form_id
        if not self.form_template:
            self.form_template = 'easyform/simple_form.html'
        self.set_data(data, errors)
            
    def __str__(self):
        form = forms.FormWrapper(self.manipulator, self.data, self.errors)
        form.buttons = self.buttons
        form.path = self.path
        form.enctype = self.enctype()
        form.form_id = self.form_id
        t = loader.get_template(self.form_template)
        c = {
            'form': form,
        }
        return t.render(Context(c))
    
    def has_filefield(self):
        for f in self.manipulator.fields:
            if isinstance(f, forms.FileUploadField):
                return True
        return False
    
    def enctype(self):
        if self.has_filefield():
            return 'enctype="multipart/form-data"'
        else:
            return ''
            
    def set_data(self, data=None, errors=None):
        self.data = data
        if not self.data:
            self.data = {}
        self.errors = errors
        if not self.errors:
            self.errors = {}
            
    def set_path(self, path):
        self.path = path
        
    def set_buttons(self, buttons):
        self.buttons = buttons
    
    def validate(self, request):
        if request.POST:
            self.data = request.POST.copy()
            self.errors = self.manipulator.get_validation_errors(self.data)
            if not self.errors:
                return True
            else:
                return False
        else:
            raise NoData, 'There is no data need to validate'
            
    def validate_and_save(self, request):
        if request.POST:
            self.data = request.POST.copy()
            self.errors = self.manipulator.get_validation_errors(self.data)
            if not self.errors:
                self.manipulator.do_html2python(self.data)
    
                self.manipulator.save(self.data)
                
                return True
            else:
                return False
        else:
            raise NoData, 'There is no data need to validate'

def validate_form(request, form, view_template, success_template='', fail_template=''):
    assert view_template, 'view_template cannot be empty'
    
    if not success_template:
        success_template = view_template
    if not fail_template:
        fail_template = view_template
        
    try:
        if form.validate_and_save(request):
            flag = SUCCESS
            template = success_template
        else:
            flag = FAIL
            template = fail_template
    except NoData:
        flag = NORMAL
        template = view_template
        
    return flag, template

def auto_render_form_to_response(request, form, view_template, success_action='', fail_action='', 
        form_variable_name='form', context={}):
    flag, template = validate_form(request, form, view_template, success_action, fail_action)
    c = {}
    c.update(context)
    c.update({form_variable_name: form})
    if isinstance(template, Action):
        return template(c)
    else:
        return render_to_response(template, c)
    
######################### Other function #######################
def get_model_data(model):
    return model.__dict__

def fix_model_manipulator(manipulator, exclude=[]):
    opts = manipulator.model._meta
    for f in manipulator.fields[:]:
        name = f.field_name
        if name in exclude:
            del manipulator[name]
        else:
            try:
                field = opts.get_field(name)
                f.verbose_name = field.verbose_name
            except:
                f.verbose_name = name.capitalize()

