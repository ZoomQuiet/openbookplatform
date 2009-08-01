扩展源代码
=====================

本文主要对项目的源代码组织结构进行一个简单的介绍。

主要项目文件及目录
-------------------

* **trans_urls.py及trans_views.py:** 这两个文件共同组成了翻译管理后台的主要功能，从trans_urls.py的urlpatterns也可以对后台翻译管理的功有一个整体的了解。

* **utils.py:** 这个文件中主要包含了会被其他各个代码文件使用的公共函数。

* **management/commands/update_doc.py:** 下载／更新文档的django命令 ``update_doc`` 的代码文件，该文件的主要工作就是通过 ``utils.py`` 中的 ``get_update_handlers`` 得到真正用来更新项目的函数。
  ``get_update_handlers`` 先从路径 ``doc_trans.update_handlers.projects.%s_handler`` 
  （%s表示项目的slug，并且 ``-`` 转换为 ``_`` 的形式,下同）尝试导入项目特殊的 ``update_handler`` 。
  如果没找到的话，再尝试从 ``doc_trans.update_handlers.%s`` (%s表示 ``Repository type`` 类型的 ``update_handler`` )导入。
  通过此种方式，就可以即为某个项目写专门的 ``update_handler`` ，再没有提供时，则使用通用的  ``update_handler`` 。后面的介绍的其他命令也运用了很多这种导入方式，可以通过源代码查看详细的导入路径。

* **management/commands/sync_doc.py:** 同步文档到数据库的django命令 ``sync_doc`` 的代码文件，在该文件中主要有3个函数 ``handle_page_added`` , ``handle_page_deleted`` , ``handle_page_modified`` 分别用来处理文档文件的添加，删除，修改3种变化状态。
  同时这些函数中还调用了 ``utils.py`` 中的 ``get_file_handler`` 来完成对各种格式的文档进行分段，重组的完整性检查等功能。
  
* **management/commands/export_doc.py:** 同步文档到数据库的django命令 ``export_doc`` 的代码文件，该文件主要是先通过  ``utils.py`` 中的 ``get_export_handler`` 将数据库中的翻译重组成全文，然后导出到文档目录。
  然后通过  ``utils.py`` 中的 ``get_exported_after_handler`` 将导出的中英文文档编译成HTML格式，以便读者的直接浏览。
  可以从目录 ``export_handlers/after_handlers/projects`` 中看到，在这里几乎为所有当前支持的文档项目写了专门的 ``get_exported_after_handler`` ，主要有以下原因：
	
	* **Sphinx版本问题：** 很多Python项目使用了不同的Sphinx版本，并且彼此不兼容，所以需要在某些项目导出前修改 sys.path 以使 0.6.2 版本的Sphinx比默认的0.5.2版本先导入。
	* **Sphinx的配置文件conf.py的问题：** 很多Python项目会在 conf.py 中导入自己项目的一些模块，以读取当前版本，CHANGELOG，等信息写到文档中，所以对这些也需要额外的处理。
	* **其他各种奇怪的问题：** Sphinx文档的导出经常会出现各种编译错误，所以差不多要为每个项目写专门的 ``get_exported_after_handler`` 。

Sphinx类型文档的编译
--------------------------------

* **Sphinx类型文档的编译:** 在这里并没有使用常用的 ``make html`` 命令或 ``sphinx-build`` 命令，而是通过函数调用的方式，该方式借鉴自django的官方网站的文档的编译方式： http://code.djangoproject.com/browser/djangoproject.com/djangodocs/bin/update-docs.py

* **即时编译的实现:** 在Web页面上的每一个翻译的提交都会即时重新编译相应的中文文档，这主要是通过 ``models.py`` 中Page Model的re_build_translation方法实现的。该方法也是通过   ``utils.py`` 中的 ``get_exported_after_handler`` 得到编译用的处理器，但是会传一个额外的参数，即需要导出的单个页面，而不是真个项目文档的所有页面。在 各个 ``get_exported_after_handler`` 看到有这个参数时，需要特别处理，以便最快速度的编译单个文档，而不需要重建所有的临时文件。对于Sphinx类型的文档而言就是在最后追加这单个文件的路径为参数。
