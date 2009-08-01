# -*- coding: utf-8 -*-
from django.contrib import admin

from doc_trans.models import Project, Page, Paragraph, Translation, Version, PageChange

   
class ProjectAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Project._meta.fields]
    prepopulated_fields = {"slug": ("name",)}

class PageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Page._meta.fields]
    

class ParagraphAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Paragraph._meta.fields]
    
    
class VersionleAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Version._meta.fields]

   
class PageChangeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PageChange._meta.fields]
    
  
class TranslationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Translation._meta.fields]
    

admin.site.register(Project, ProjectAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Paragraph, ParagraphAdmin)
admin.site.register(Version, VersionleAdmin)
admin.site.register(PageChange, PageChangeAdmin)
admin.site.register(Translation, TranslationAdmin)
