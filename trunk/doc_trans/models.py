# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from doc_trans.settings import REPOSITORY_TYPES, DOC_TYPES, PAGE_CHANGE_ACTION_TYPES
from doc_trans.utils import get_file_handler, get_exported_after_handler
import datetime
import os
import re
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

class Project(models.Model):
    name = models.CharField(max_length = 250, unique = True)
    slug = models.SlugField(max_length = 250)
    project_description = models.TextField(blank = True)
    repository_url = models.CharField(max_length = 250)
    repository_type = models.CharField(max_length = 50, choices = REPOSITORY_TYPES, default = 'svn')
    doc_type = models.CharField(max_length = 50, choices = DOC_TYPES, default = 'sphinx')
    exclude_dir_names = models.CharField(max_length = 250, blank = True, help_text = u"Regular expression splited by space")
    doc_file_extensions = models.CharField(max_length = 250, blank = True)
    doc_dir_name = models.CharField(max_length = 250, blank = True, help_text = u"Only used for hg, where is docs dir in the project repository")
    created = models.DateTimeField(auto_now_add = True)
    translators = models.ManyToManyField(User, related_name = "joined_projects", null = True, blank = True)
#    history_translators = models.ManyToManyField(User, related_name = "translatd_projects", null = True, blank = True)
    suspended = models.BooleanField(default = False)
    
    
    def page_contents(self, path = None):
        content_type_id = ContentType.objects.get_for_model(Page).id
        site_id = settings.SITE_ID
        effective_pages = self.current_pages.select_related(depth=1).extra(
            select={
                'paragraph_count': 'SELECT COUNT(*) FROM doc_trans_paragraph WHERE doc_trans_page.id = doc_trans_paragraph.page_id AND doc_trans_paragraph.current_version_id = doc_trans_page.current_version_id',
                'translated_count': 'SELECT COUNT(DISTINCT doc_trans_paragraph.id) FROM doc_trans_paragraph INNER JOIN doc_trans_translation ON (doc_trans_paragraph.id = doc_trans_translation.paragraph_id) WHERE (doc_trans_paragraph.current_version_id = doc_trans_page.current_version_id  AND doc_trans_paragraph.page_id = doc_trans_page.id  AND doc_trans_translation.id IS NOT NULL)',
                'comment_count': 'SELECT COUNT(*) FROM django_comments WHERE django_comments.site_id = %s  AND django_comments.object_pk = doc_trans_page.id  AND django_comments.content_type_id = %s  AND django_comments.is_public = True  AND django_comments.is_removed = False' % (site_id, content_type_id),
            },
        )
        if path and not path.endswith('/'): path = path + '/'
        content_dict = {}
#        effective_pages = self.current_pages.select_related(depth=1)
        if path:
            effective_pages = effective_pages.filter(path__istartswith = path)
        for page in effective_pages:
            section = content_dict.setdefault(page.section_slug(path),[])
            section.append(page)
        content = []
        for section in content_dict:
            content_dict[section].sort(key = lambda e: e.path)
            content.append((section, content_dict[section]))
        content.sort(key = lambda e: e[0])
        
        return content
    
    
    @property
    def latest_version(self):
        if hasattr(self, '_latest_version'):
            return self._latest_version
        else:
            self._latest_version = self.versions.latest('created')
            return self._latest_version
    
    @property
    def current_pages(self):
        return Page.objects.filter(project = self, current_version = self.latest_version, deleted = False)
    
    @property
    def current_paragraphs(self):
        current_pages = self.current_pages
        latest_version = self.latest_version
        return Paragraph.objects.filter(page__in = current_pages, current_version = latest_version)
    
    class Meta:
        verbose_name = u"project"
        verbose_name_plural = u"projects"
        
    def __unicode__(self):
        return  self.name
    
    @property
    def root(self):
        return os.path.join(settings.DOCS_DIR, self.slug)
    
    @property
    def doc_path(self):
        return os.path.join(settings.DOCS_DIR, self.slug, settings.ORIGINAL_LANGUAGE)
    
    @property
    def export_path(self):
        return os.path.join(settings.DOCS_DIR, self.slug, settings.TRANSLATION_LANGUAGE)
    
    @property
    @models.permalink
    def join_url(self):
        return ('doc_trans-trans-project-join-quit', [self.slug, 'join'])
    
    @property
    @models.permalink
    def quit_url(self):
        return ('doc_trans-trans-project-join-quit', [self.slug, 'quit'])
    
    @property
    @models.permalink
    def page_list_url(self):
        return ('doc_trans-trans-project-page-list', [self.slug,])
    
    @property
    @models.permalink
    def view_url(self):
        return ('doc_trans-docs-project-index', [self.slug,])
    
    @property
    @models.permalink
    def view_original_url(self):
        return ('doc_trans-docs-project-serve', [self.slug, settings.ORIGINAL_LANGUAGE])
    
    @property
    @models.permalink
    def view_translated_url(self):
        return ('doc_trans-docs-project-serve', [self.slug, settings.TRANSLATION_LANGUAGE])
    
    
    @property
    @models.permalink
    def versions_url(self):
        return ('doc_trans-trans-project-versions', [self.slug,])
    
    @property
    @models.permalink
    def comments_url(self):
        return ('doc_trans-trans-project-comments', [self.slug,])
    
    
    def is_doc_file(self, path):
#        extensions = [".txt",'.rst']
        extensions = []
        extensions.extend([n.lower() for n in self.doc_file_extensions.split()])
        exclude_dirs = []
        exclude_dirs.extend([n for n in self.exclude_dir_names.split()])
        path = path.replace('\\', '/')
        for exclude_dir in exclude_dirs:
            if re.match(exclude_dir, path):
                return False
#        dir_name, basename = os.path.split(path)
#        bits = dir_name.split('/')
#        for bit in bits:
#            if bit.startswith("_") or bit.startswith(".") or bit.lower() in exclude_dirs:
#                return False
        filename, extension = os.path.splitext(path)
        if extension.lower() in extensions:
            return True
        return False

class Version(models.Model):
    last_version = models.OneToOneField('self', related_name = "next_version", null = True, blank = True)
    project = models.ForeignKey(Project, related_name = "versions")
    revision = models.CharField(max_length = 250)
    created = models.DateTimeField(auto_now_add = True)
    
    @property
    @models.permalink
    def detail_url(self):
        return ('doc_trans-trans-project-version', [self.project.slug, self.revision])
    
    class Meta:
        verbose_name = u"version"
        verbose_name_plural = u"versions"
    
    def __unicode__(self):
        return  self.revision
    
class Page(models.Model):
    project = models.ForeignKey(Project, related_name = "pages")
    path = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250)
    doc_type = models.CharField(max_length = 50, choices = DOC_TYPES)
    current_version = models.ForeignKey(Version, related_name = "pages")
    created = models.DateTimeField(auto_now_add = True)
    deleted = models.BooleanField(default = False)
    
    @property
    def current_paragraphs(self):
        return Paragraph.objects.filter(page = self, current_version = self.current_version)
    
    @property
    def translated_paragraphs(self):
        if hasattr(self, '_translated_paragraphs'):
            return self._translated_paragraphs
        else:
            self._translated_paragraphs = Paragraph.objects.filter(page = self, current_version = self.current_version, translations__isnull = False).distinct()
            return self._translated_paragraphs
      
    @property
    def translated_and_reviewd_paragraphs(self):
        paragraphs = []
        for p in self.translated_paragraphs:
            if p.latest_translation.reviewed:
                paragraphs.append(p)
        return paragraphs
      
    
    @property
    @models.permalink
    def trans_url(self):
        return ('doc_trans-trans-page-trans', [self.project.slug, self.slug,])
    
    @property
    @models.permalink
    def changes_url(self):
        return ('doc_trans-trans-page-changes', [self.project.slug, self.slug,])
    

    @models.permalink
    def view_url(self, lang = settings.TRANSLATION_LANGUAGE):
        if self.doc_type == 'sphinx':
            path = os.path.splitext(self.path)[0] +'.html'
            return ('doc_trans-docs-project-serve', [self.project.slug, lang + '/' + path])
        if self.doc_type == 'textile' and self.project.name == 'Rails Guides':
            path = (os.path.splitext(self.path)[0] +'.html').replace('source/', '')
            return ('doc_trans-docs-project-serve', [self.project.slug, lang + '/' + path])
        return ('doc_trans-docs-project-serve', [self.project.slug, lang + '/' + self.path])
    
    @property
    def view_original_url(self):
        return self.view_url(settings.ORIGINAL_LANGUAGE)
    
    @property
    def view_translated_url(self):
        return self.view_url(settings.TRANSLATION_LANGUAGE)
    
    @property
    @models.permalink
    def comments_url(self):
        return ('doc_trans-trans-page-comments', [self.project.slug, self.slug,])
    
    
    def section_slug(self, path = None):
        if path:
            self.path = self.path.replace(path, '')
        if '/' in self.path:
            return self.path.split('/')[0]
        else:
            return ''
    
    
    class Meta:
        verbose_name = u"page"
        verbose_name_plural = u"pages"
    
    def save(self, force_insert=False, force_update=False):
        if not self.doc_type:
            self.doc_type = self.project.doc_type
        self.slug = slugify(self.path.replace('/', '-').replace('.', '-').replace('_', '-'))
        super(Page, self).save(force_insert, force_update)
    
    def write_page(self):
        exprot_dir = os.path.join(settings.DOCS_DIR, self.project.slug, settings.TRANSLATION_LANGUAGE)
        paragraph_objects = self.current_paragraphs.order_by('ordinal')
        page_file = open(os.path.join(exprot_dir, self.path), 'w')
        translations =[p.original_or_translation for p in paragraph_objects]
        file_handler = get_file_handler(self)
        file_content = file_handler.concat_translations(translations)
        file_content = file_content.encode('utf-8')
        page_file.write(file_content)
        page_file.close()
        
    def re_build_translation(self):
        self.write_page()
        exported_after_handler = get_exported_after_handler(self.project)
        exported_after_handler.handle_exported(self.project, settings.TRANSLATION_LANGUAGE, self)
        
    def check(self):
        file_handler = get_file_handler(self)
        paragraphs_in_db = Paragraph.objects.filter(page = self, current_version = self.current_version).order_by('ordinal')
        for i, paragraph in enumerate(paragraphs_in_db):
            if i+1 != paragraph.ordinal:
                raise ValidationError, u"page '%s' ordinals didn't continuous in db\n\n%s\n\n" % (self.path, ",".join(str(o) for o in paragraphs_in_db.values_list('ordinal', flat=True)))
            
        page_content = open(os.path.join(self.project.doc_path, self.path)).read()
        file_handler.compare(page_content, file_handler.concat(paragraphs_in_db), self)

    def __unicode__(self):
        return  self.slug
    
class Paragraph(models.Model):
    page = models.ForeignKey(Page, related_name = "paragraphs")
    current_version = models.ForeignKey(Version, related_name = "paragraphs")
    created = models.DateTimeField(auto_now_add = True)
    original = models.TextField()
    ordinal = models.IntegerField()
    history_paragraph = models.OneToOneField('self', related_name = "modified_paragraph", null = True, blank = True)
  
    @property
    @models.permalink
    def translation_url(self):
        return ('doc_trans-trans-paragraph-translation', [self.id,])
    
    @property
    @models.permalink
    def histories_url(self):
        return ('doc_trans-trans-paragraph-histories', [self.id,])
    
    @property
    @models.permalink
    def comments_url(self):
        return ('doc_trans-trans-paragraph-comments', [self.id,])
    
    @property
    @models.permalink
    def translation_histories_url(self):
        return ('doc_trans-trans-paragraph-translation-histories', [self.id,])
    
    
    @property
    def cols(self):
        return max(max(len(line) for line in self.original.splitlines()), 80) + 10
    
    @property
    def rows(self):
        return len(self.original.splitlines()) + 2
    
    @property
    def latest_translation(self):
        if hasattr(self, '_latest_translation'):
            return self._latest_translation
        else:
            try:
                self._latest_translation = self.translations.latest('created')
            except Translation.DoesNotExist:
                self._latest_translation = None
            return self._latest_translation
    
      
    @property
    def history_paragraphs(self):
        paragraphs = [self, ]
        base_paragraph = self
        while base_paragraph.history_paragraph:
            paragraphs.append(base_paragraph.history_paragraph)
            base_paragraph = base_paragraph.history_paragraph
        paragraphs.reverse()
        return paragraphs
    
    @property
    def original_or_translation(self):
        translation = self.latest_translation
        if translation:
            return translation.content
        else:
            return self.original
        
    class Meta:
        verbose_name = u"paragraph"
        verbose_name_plural = u"paragraphs"
    
    def __unicode__(self):
        return  self.original.splitlines()[0][:50]
    
class Translation(models.Model):
    paragraph = models.ForeignKey(Paragraph, related_name = "translations")
    history_translation = models.OneToOneField('self', related_name = "modified_translation", null = True, blank = True)
    translator = models.ForeignKey(User, related_name = "translations")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    ip = models.IPAddressField()
    location = models.CharField(max_length = 50, blank = True)
    
    reviewed = models.BooleanField(default = False)
    reviewed_by = models.ForeignKey(User, null = True, blank = True)
    reviewed_at = models.DateTimeField(null = True, blank = True)
    
    @property
    def history_translations(self):
        translations = [self, ]
        base_translation = self
        while base_translation.history_translation:
            translations.append(base_translation.history_translation)
            base_translation = base_translation.history_translation
        translations.reverse()
        return translations
    
    class Meta:
        verbose_name = u"translation"
        verbose_name_plural = u"translations"
    
    def __unicode__(self):
        return  u"Translation %s for paragraph %s" % (self.id, self.paragraph.id)
    
class PageChange(models.Model):
    page = models.ForeignKey(Page, related_name = "changes")
    version = models.ForeignKey(Version, related_name = "changes")
    paragraphs = models.ManyToManyField(Paragraph, related_name = "changes", null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True)
    action = models.CharField(max_length = 50, choices = PAGE_CHANGE_ACTION_TYPES, default = 'modified')
    
    @property
    @models.permalink
    def detail_url(self):
        return ('doc_trans-trans-page-version-changes', [self.page.project.slug, self.page.slug, self.version.revision])
    
    
    class Meta:
        verbose_name = u"page change"
        verbose_name_plural = u"page changes"
        
    def __unicode__(self):
        return  u"page %s change at version %s" % (self.page, self.version)