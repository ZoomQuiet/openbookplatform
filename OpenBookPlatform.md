![http://www.woodpecker.org.cn/share/projects/OpenBookPlatform.png](http://www.woodpecker.org.cn/share/projects/OpenBookPlatform.png)

# Thinking #

来源自:
[OpenBookProject](http://code.google.com/p/openbookproject)
![http://www.woodpecker.org.cn/share/projects/OpenBookProject-default.png](http://www.woodpecker.org.cn/share/projects/OpenBookProject-default.png)

## 当前建议 ##
对比 The Django Book
  * http://djangobook.py3k.cn/

实际上这种形式历史上有好几个:
统一的特性是:
  * 使用 Django 作为开发框架
  * 使用 DB 来存储内容和翻译以及其它信息
  * 翻译针对段落 ,比照进行
  * 有丰富的统计功能

但是,从俺的翻译体验来看,不推荐这种形式!推荐:
  * 关于本书的编写 — 用Python做科学计算 http://hyry.dip.jp/pydoc/pydoc_write_tools.html
  * PyMOTW 中文版! — PyMOTW Document v1.6 documentation http://www.vbarter.cn/pymotw/

即:
  * 作者/译者,通过版本管理系统进行協作
  * 作者/译者,面对的是章节为单位的整体文本(结构化文本, rST),可以自由的在自个儿喜欢的编辑器中进行编辑,并整体调节段落
  * 作者/译者,可以随时在本地看到图书网站的全貌

对于整个平台的创建;
Django 类依赖DB 的服务:
```
- 复杂,部署环境很难找,或是成本高
- 复杂,出现问题后,追踪和解决也比较困难
- 复杂,难以根据需要快速增补辅助功能
```
俺推荐的通过 Sphinx 自动化组织 rST 成为图书网站的方式:
```
- 简单,服务端可以不部署任何动态应用,纯粹 HTML 页面发现就好:
    - 评注可以使用免费的JS 嵌入式评注服务
    - 也可以使用 自行部署的Ajax 式评注服务
    - 最直接的是通过 邮件进行收集意见
- 简单,备份/迁移/恢复,都非常简单,一键完成
- 简单,所有扩展都是针对静态HTML 文本进行,和翻译平台没有关系
```
那么,"现代软件工程"以及后续的 yeka新图书团队的开放式在线图书平台的实现过程,俺建议:
```
+ 使用 BitBucket.org 在线工程服务
+ 使用 Free Hosting at BitBucket 空间服务来发布最终图书
    http://hgtip.com/tips/beginner/2009-10-13-free-hosting-at-bitbucket/
+ 图书团队本身不用管理/购买任何空间服务,也不用部署任何在线系统,就直接约定好流程就可以开张了:
    1. 在BitBucket.org 注册帐号, 比如说 YekaTechBook 最好是公司或是团队名
    2. 开辟图书仓库 https://bitbucket.org/YekaTechBook/现代软件工程 (当然不应该使用中文)
    3. 初始化 Sphinx 工程 参考:SphinxprojectHowto - pymotwcn
        http://code.google.com/p/pymotwcn/wiki/SphinxprojectHowto
    4. 将工程加入到 图书仓库中
    5. 在图书仓库的维基中,详细说明如何协同/本地编译/rST 使用,发布给作者们
    6. 定期在 lispython 或是谁的机器上检出作者们的修订,编译成HTML 发布到图书发布空间
        http://现代软件工程.BitBucket.org/
        当然,可以使用新公司的域名来指向这里
        比如说,俺主持的相关图书翻译,已经在这么作了:
        http://zoomquiet.org/
```

以上!
这样部署图书在线翻译工程的代价:
  * 相关作者要学习使用 rST (Sphinx 不一定需要使用)
  * 相关作者要学习使用 Hg
获得的好处:
  * 最小的部署成本(零成本,除了公司域名每年要的费用,也不用专门的技术人员来维护)
  * 最稳定的运营质量(发布/备份/迁移/升级,全部一键搞定)
  * 可以离线工作,不依赖网络,可以在本地进行版本管理,编译,甚至于进行小范畴的協同,交换成果

相比自主研发的在线 web 服务式的翻译平台:

- 代价:
  * 需要主机空间/流量/IP 等等资源的支出(除非有 GAE 版本,但是也无法保证永远可用)
  * 需要专门技术团队来维护,修补
  * 运营品质,看技术团队的人品和能力
  * 作者/译者,要忍受被自动切分的段落化翻译流程,无法自由的为中文,调整摧残层次
  * 依赖系统和网络,一但网络出现问题,或是主机出现问题,整个平台将无法使用
- 好处:
  * 用户/作者,都没有学习成本,直接可用