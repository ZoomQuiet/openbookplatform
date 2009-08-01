安装
=========

源代码是以标准的Django App形式组织的。可以通过svn从::

    svn checkout http://openbookplatform.googlecode.com/svn/trunk/doc_trans doc_trans

下载到。

安装需求
-------------

* **Linux/Windows** :推荐使用Linux，因为项目是在Linux下开发并测试完成的，Windows下没有经过足够的运行测试。
* **Python 2.5** :因为是在该Python版本下开发的，其他版本的Python未经过测试。
* **Django svn版本** :注意，并不兼容1.0版本的django，因为使用了Model的Aggregation功能，这个是在svn版本中才有的。
* **pysvn 1.7.0或以上** 
	
	* Windows 版本下载地址::
	
		http://pysvn.tigris.org/servlets/ProjectDocumentList?folderID=5840&expandFolder=5840&folderID=1768
  	   
  	 下载后直接双击安装即可。
  	   
  	* Linux版本需要从源代码编译安装，编译前需要满足pysvn本身的依赖要求，我在ubuntu8.04上编译是遇到一个链接错误，不知道是不是我漏掉了某个库。最后通过修改Makefile文件的第14行::
  	
  		LDLIBS=-L/usr/lib -Wl,--rpath -Wl,/usr/lib -lsvn_client-1 -lsvn_diff-1 -lsvn_repos-1 -lcom_err -lresolv -lexpat -lneon -lssl
  		
  	  为::
  	
  		LDLIBS=-L/usr/lib -Wl,--rpath -Wl,/usr/lib -lsvn_client-1 -lsvn_diff-1 -lsvn_repos-1 -lcom_err -lresolv -lexpat -lssl
  	
  	  编译通过。

* **pygments** :因为通过Web方式进行翻译提交时，需要高亮对照显示原文，所以还需要安装pygments。

* **Sphinx 0.5.2** :注意，Sphinx目前的最新版是0.6.2，但是某些项目的Sphinx类型的文档只支持0.5.2，
  而有些只支持0.6.2以上，所以在这里通过默认安装版本为0.5.2，但是如果某个项目的文档要求是0.6.2，
  就通过修改sys.path的方式切换到0.6.2版本。

* **jinja** :注意不是jinja2，而是jinja，Sphinx类型的文档在输出HTML格式的文档需要调用jinja模板。

* **mercurial** :如果所需要翻译的项目文档是存在mercurial版本控制系统上的话，还需要安装mercurial，只要使 ``import mercurial`` 可以导入或 ``hg`` 命令可用就可以了，因为windows下编译mercurial比较麻烦。


安装过程
---------------

1. 首先从svn下载源码，并放到任何Python Path可见的地方，即使 ``import doc_trans`` 可用。
2. 在你所在的Django项目的setting.py文件中添加以下设置:

	1. 在 ``INSTALLED_APPS`` 中加入该app ``‘doc_trans’`` 。
	2. 其他设置::
		
		PRO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ))
		DOCS_DIR = os.path.abspath(os.path.join(PRO_PATH, '..', 'docs_repository'))
		ORIGINAL_LANGUAGE = 'en'
		TRANSLATION_LANGUAGE = 'zh-cn'
		HG_REPO_NAME = 'hg'
		WEB_DOCS_DIR = os.path.abspath(os.path.join(PRO_PATH, '..', 'web_docs_repository'))
		SVN_DOCS_DIR = os.path.abspath(os.path.join(PRO_PATH, '..', 'svn_docs_repository'))
		SVN_DOCS_BACKUP_DIR = os.path.abspath(os.path.join(PRO_PATH, '..', 'svn_docs_repository_backup'))
		
		if os.name == 'nt':
		    LOCAL_SVN_URL = 'file:///%s/' % SVN_DOCS_DIR.replace('\\', '/')
		else:
		    LOCAL_SVN_URL = 'file://%s/' % SVN_DOCS_DIR
    
	  以上这些设置的一些说明。
      	  
       	* **DOCS_DIR:** 是用来存放各个项目的文档的目录，包括svn，及其他各种来源的英文文档， 从数据库中导出的中文文档。
       	* **ORIGINAL_LANGUAGE:** 这个网站所翻译的文档的原始语言的名字，可以为其他各种命名方式，只是该字符串也将被用作 ``DOCS_DIR`` 目录下存放原文文档的目录名。
       	* **TRANSLATION_LANGUAGE:** 这个网站所翻译的文档的目标语言的名字，可以为其他各种命名方式，只是该字符串也将被用作 ``DOCS_DIR`` 目录下存放目标语言文档的目录名。
       	* **HG_REPO_NAME:** 由于很多Python项目使用了mercurial作为版本控制系统，但是mercurial不提供单个目录的下载方式，所以要先将整个项目下载下来存放到此名字的临时目录下，然后再从此目录下拷贝出实际的文档目录。
       	* **WEB_DOCS_DIR:** 用来存放各个项目导出的英文，中文文档的HTML格式文档的目录路径。
       	* **SVN_DOCS_DIR:** 用来存放以非svn方式作为版本控制系统的项目的原文文档的版本仓库路径，此目录应该使用 ``'svnadmin create some_name'`` 的形式创建。
       	* **SVN_DOCS_BACKUP_DIR:** 用来存放对 ``SVN_DOCS_DIR`` 仓库进行自动备份的的备份文件目录，再每次要对 ``SVN_DOCS_DIR`` 仓库进行提交时都会进行一次自动的备份。
       	* **LOCAL_SVN_URL:** 用来将 ``SVN_DOCS_DIR`` 的本地路径形式转换为SVN所使用的本地仓库路径形式。
       	
	3. 可选设置，如果你想将你网站界面所可选的语言限制一定范围内，可设置django提供的 ``LANGUAGES`` 选项::
		
		LANGUAGES = (
		    ('en', u'English'),
		    ('zh-cn', u"简体中文"),
		)
		
	4. 以上就是添加 ``doc_trans`` 这个app所需要的全部设置。
	
4. 在 ``urls.py`` 文件加入本app的urls::
	
	urlpatterns = patterns('',
	    # Example:
	    #.........................
	    (r'^trans/', include('doc_trans.trans_urls')),
	    (r'^docs/', include('doc_trans.urls')),
	)

   这里有两个urls.py文件需要include：
     
  * ``urls.py`` 主要是项目列表浏览及查看HTML版本的文档浏览。
  * ``trans_urls.py`` 主要是翻译的后台管理，比如翻译提交，项目进度查看等。
	
5. 在配置好以上这些设置后，还需要运行 ``python manage.py syncdb`` 命令，同步本app所需要的数据库结构。
	
       	
更新，同步，导出文档
-----------------------

在安装好本app后，现在数据库中还没有任何可翻译的项目，接下来将如何创建翻译项目。

1. 首先，打开你的Django admin 后台，可以看到多了这个app所添加的可管理的Model，打开其中的 ``Projects`` Model进行项目的添加。
2. 项目添加说明:
	
	* **Name:** 项目的名字。
	* **Slug:** 项目的Slug,注意不要太复杂，因为这不但会作为项目存放文档的路径名，而且还会作为同步文档时的命令行参数以及编写可扩展代码的一部分文件名。
	* **Project description:** 项目的基本描述。
	* **Repository url:** 项目文档的存放路径，目前支持3种方式:
	
		* **svn:** 比如Django 文档的路径为 ``http://code.djangoproject.com/svn/django/trunk/docs/`` 。注意，最后的 **docs/** ，这是必须的，因为文档是存放在该目录下。
		* **hg:** 比如Sphinx 文档的路径为 ``http://bitbucket.org/birkenfeld/sphinx/`` 。注意，最后末尾并没有  **doc/** ， 因为hg只能以整个项目的形式下载，所以为了表示文档存放在哪个路径，还需要将文档目录名填写到后面的 **Doc dir name** 这个参数。
		* **本地文档类型:** 比如 Google App Engine 文档的路径只是简单的一个目录名为 ``google-appengine-docs-20090508`` 。但是你需要额外的步骤使这个目录名有意义，比如先从 http://code.google.com/p/googleappengine/downloads/list 下载 google-appengine-docs-20090508.zip 这个压缩包，然后在 ``DOCS_DIR`` 下新建以 project slug 为名字的目录，然后将压缩包解压为 google-appengine-docs-20090508 ，即 **Repository url** 中所填的路径名。
		  
	* **Repository type:** 项目文档所存放的类型选择。
	* **Doc type:** 项目文档所使用的文本格式， 比如Sphinx，HTML等。
	* **Exclude dir names:** 项目文档目录中，通过空格分离的正则表达式，显式指定某些目录中的所有文件都不作为文档文件，比如 Google App Engine 文档不需要翻译 java doc ，此正则表达式为 ``appengine/docs/java/javadoc/.+`` 。此项通常不需要设置，因为后面还需要指定 **Doc file extensions** 。
	* **Doc file extensions:** 项目文档文件所使用的文件扩展名，比如Django的为 ``.txt`` , Sphinx的为 ``.rst`` ,注意点号并不能省略。多个文件扩展名之间可以用空格隔开。
	* **Doc dir name::** 如果文档的来源类型是 hg， 那么此处需要填写文档目录所在的文件夹名。

3. 在将项目信息添加到数据库后，就可以开始同步文档，这是通过3个相关的Django命令实现的，分别是 update_doc, sync_doc, export_doc . 下面分别按项目文档翻译的流程顺序介绍这3个命令。

4. update_doc::
	
	python manage.py update_doc project-slug [-r]

  该命令的主要作用是根据项目信息，从远程服务器上或本地文档目录，下载／更新本地的英文文档到指定版本。如果为非svn类型的文档来源，还会自动提交改变到本地的一个svn服务器。
  该命令接受一个项目的slug作为参数，同时还有一个可选参数  ``-r`` ，表示要同步到的版本，不填的话表示更新最新版本。
  该命令不涉及任何的数据库写操作，只是简单的对文档目录进行更新，所以在运行了这个命令之后还需要运行第2个命令：sync_doc


5. sync_doc::
	
	python manage.py sync_doc project-slug

  由于update_doc只涉及对文档目录的更新，还需要运行这个命令将这些更新信息同步到数据库中。
  同步版本，及文档变化信息到数据库中的这个操作，是封装在一个数据库事务中的，所以中间有任何同步不一致的情况出现，会马上进行回滚，并报告错误信息。
  之所以要将这2个步骤分开操作，主要是为了防止意外的错误导致的不一致，比如网络中断，同步错误等。


5. export_doc::
	
	python manage.py export_doc project-slug

  在文档翻译的任何过程中，都可以使用export_doc命令将文档的中英文版本导出，导出的过程包括HTML格式版本的文档生成。