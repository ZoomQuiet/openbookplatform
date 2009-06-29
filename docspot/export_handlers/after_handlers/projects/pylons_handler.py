# -*- coding: utf-8 -*-
from django.conf import settings
import os
import shutil
import pysvn
from doc_trans.export_handlers.after_handlers.sphinx_handler import build_docs

modindex = """
{% extends "layout.html" %}
{% set title = 'Global Module Index' %}
{% block extrahead %}
{% if collapse_modindex %}
    <script type="text/javascript">
      DOCUMENTATION_OPTIONS.COLLAPSE_MODINDEX = true;
    </script>
{% endif %}
{% endblock %}
{% block body %}

   <h1 id="global-module-index">Global Module Index</h1>
{% if builder == 'web' and freqentries %}
   <p>Most popular modules:</p>
   <div class="modulecloud">
   {%- for module in freqentries %}
     <a href="../q/{{ module.name|e }}/" style="font-size: {{ module.size }}%">{{ module.name|e }}</a>
   {%- endfor %}
   </div>
{% endif %}
{% if builder == 'web' %}
   <form class="pfform" action="" method="get">
     Show modules only available on these platforms:<br>
     {% for pl in platforms -%}
     <input type="checkbox" name="pf" value="{{ pl }}" id="pl-{{ pl }}"
            {%- if pl in showpf %} checked="checked"{% endif %}>
     <label for="pl-{{ pl }}">{{ pl }}</label>
     {% endfor %}
     <input type="hidden" name="newpf" value="true">
     <input type="submit" value="Apply">
   </form>
{% endif %}

   {%- for letter in letters %}
   <a href="#cap-{{ letter }}"><strong>{{ letter }}</strong></a> {% if not loop.last %}| {% endif %}
   {%- endfor %}
   <hr/>

   <table width="100%" class="indextable" cellspacing="0" cellpadding="2">
   {%- for modname, collapse, cgroup, indent, fname, synops, pform, dep in modindexentries %}
   {%- if not modname -%}
   <tr class="pcap"><td></td><td>&nbsp;</td><td></td></tr>
   <tr class="cap"><td></td><td><a name="cap-{{ fname }}"><strong>{{ fname }}</strong></a></td><td></td></tr>
   {%- else -%}
   <tr{% if indent %} class="cg-{{ cgroup }}"{% endif %}>
     <td>{% if collapse -%}
       <img src="{{ pathto('_static/minus.png', 1) }}" id="toggle-{{ cgroup }}"
            class="toggler" style="display: none" />
         {%- endif %}</td>
     <td>{% if indent %}&nbsp;&nbsp;&nbsp;{% endif %}
     {% if fname %}<a href="{{ fname }}">{% endif -%}
     <tt class="xref">{{ modname|e }}</tt>
     {%- if fname %}</a>{% endif %}
   {%- if pform[0] %} <em>({{ pform|join(', ') }})</em>{% endif -%}
   </td><td>{% if dep %}<strong>Deprecated:</strong>{% endif %}
     <em>{{ synops|e }}</em></td></tr>
   {%- endif -%}
   {% endfor %}
   </table>

{% endblock %}
"""
def handle_modindex(problem_file_name):
    problem_file = open(problem_file_name, 'w')
    problem_file.write(modindex)
    problem_file.close()
       
def handle_exported(project, language = None, page = None):
    web_docs_repository_path = os.path.join(settings.WEB_DOCS_DIR, project.slug, )
    doc_dir =  os.path.join(web_docs_repository_path, settings.ORIGINAL_LANGUAGE)
    exprot_dir = os.path.join(web_docs_repository_path, settings.TRANSLATION_LANGUAGE)
    
    if not page:
        temp_project_doc_path = project.doc_path + '-temp'
        client = pysvn.Client()
        client.exception_style = 1
        if os.path.exists(temp_project_doc_path):
            shutil.rmtree(temp_project_doc_path)
        client.export(project.doc_path, temp_project_doc_path)
        problem_file_name = os.path.join(temp_project_doc_path, '_templates','modindex.html')
        handle_modindex(problem_file_name)
    problem_file_name = os.path.join(project.export_path, '_templates','modindex.html')
    handle_modindex(problem_file_name)
    
    if page:
        build_docs(project.export_path, exprot_dir, page = page)
        return
    
    if language == None:
        build_docs(temp_project_doc_path, doc_dir)
        build_docs(project.export_path, exprot_dir)
    elif language == settings.ORIGINAL_LANGUAGE:
        build_docs(temp_project_doc_path, doc_dir)
    elif language == settings.TRANSLATION_LANGUAGE:
        build_docs(project.export_path, exprot_dir)
        
    