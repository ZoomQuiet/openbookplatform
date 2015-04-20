

# docspot.org 规划 #
```
项目想好，文档得全；社区想好，文档得精！
技术再好，文档不齐，没有后力，无从发展!
```
## 概述 ##
> 本文从 ZoomQuiet 个人角度针对 docspot.org 的可持续发展给出多方面的思考方向，以便联合哲思社区在进行共同发展时，有一个可以讨论的基础;

## 背景 ##
缘起::
  * [发布一个Python的协同文档翻译平台 - python-cn`CPyUG`华蟒用户组(中文Py用户组) | Google 网上论坛](http://groups.google.com/group/python-cn/browse_thread/thread/f9a128ffc548d184/bfd6676a927133a8)
  * 引发的,由 金浩 090613 分享的原创图书翻译平台:
    * http://docspot.org/

历史::
  * 早在2007 年由各种啄木鸟社区主持的图书翻译工程就已经引发了一个统一的在线图书翻译平台的项目:
    * http://wiki.woodpecker.org.cn/moin/ObpLatform
    * 由于 Limodou 兴趣转移从而停顿
  * 后来由 vcc.163 另外自主开发并发布的 pydoc-zh 计划也上线了一个在线图书翻译平台:
    * http://fy.py3k.cn
    * 依然由于没有后续运维而停顿

现状::
  * 随着 Python 技术在世界的走热,在中国,也逐渐聚集起了人气,各种领域的 Python 应用都有团队在关注和维护中文文档的翻译
  * 但是,处于零散,没有统一平台和团队/社区管理的状态!
  * 造成了在各种场合,都有新人在`月经问`**有什么好文档来自学...**

## 建议 ##
到目前为止 docspot.org 是最为完整的可以体现出文档统一平台态势的工程!
  * 为了中文技术同好们有个可以集中精力来完善的图书中心, 建议,从以下多个方面进行重构,真正向一个可持续发展的技术文档中心进化!

### 宗旨 ###
`名不正则言不顺!` ~ 没有一个鲜明的宗旨,就无法统一从设计开发到宣传推广的所有环节的思路!

思考::
  * 受众?
  * 参与者?
  * 如何永续发布?
  * 目标?

ZoomQuiet 建议:
  * 要明智的识别和区分不同的受众并提供不同的服务!
    * `内容贡献层:`
      * 这是 docspot.org 的核心成员,可以参与开发/翻译/管理 等等实质性的工作
      * 要求是有Python 开发经验,有项目管理体验,有固定的时间投入,认同文档中心理念...
      * 应该严格审查,长期联系,紧密沟通,形成团队!
    * `内容消费层:`
      * 这是 docspot.org 提供的图书内容使用人群, 可以参与宣传/反馈/镜像 等等消费和推广活动
      * 对于素质没有很高的要求,但是对于 troll 得有控制
      * 应该提供绝对 KISS 化的方便反馈渠道和最高速度的响应支持
  * 在聚集了一定的内容和贡献团队,以及固定的消费群体后,就应该可以考虑和正式媒体合作发行实体书或是其它有偿活动
  * **但是!**
    * 核心宗旨,应该是简洁明了并与当前其它类似服务有鲜明不同的!
      * e.g:
        * 译言: 自由文章翻译和发布平台
        * 科学松鼠会: 权威科普文章分享平台
      * 那么 docspot.org 应该成为:
        * **权威Python 技术中文图书平台**
        * 核心服务:
          * 高效权威的相关领域图书翻译/原创/发行支持
          * 统一方便的图书资料查阅分享
        * 即::
          * 为有能力的团队提供统一方便的图书工程组织平台
          * 为新人或是媒体,提供标准快捷的图书查阅中心
        * 所以:
          * 针对不同用户群要提供不同的界面和服务
          * 界面的设计要吻合一般性原则:
            * SEO 友好
            * 具亲合力 Dive Into Accessibility
              * http://www.woodpecker.org.cn/share/doc/DiA/diveintoaccessibility-zh/
  * 后续运营合作,建议选择 哲思自由软件社区:
    * http://www.zeuux.org/about/about.cn.html
    * 因为可以借重发布的 http://www.zeuux.com 哲思SNS平台建立可 mushup 化的服务!
      * 详细的请 Bill Xu 后续讨论


### 组织 ###
`综上,想快速转变当前无管理的个人作品网站形象,形成可持续发展的态势,第一要点,就是建立有统一思路的团队!`

  * 有固定活动场所/目标/计划/角色 的人群,才算组织!
  * 应该有规划性的配置不同专职角色成员来担当各方面职责

ZoomQuiet 建议::
  * 核心团队:
    * 主持人: 1~2 人,作为整个项目的管理者,统一发展策略和方向
    * 开发者: 1~3 人,作为平台的主力开发,对平台的品质负责
    * 运维者: 1~2 人,对主机安全/健康负责,同时进行配置管理的支持
  * 外部团队:
    * 各种己有技术团队团队
      * 通过沟通/协商,或是并入 docspot.org 平台发布图书,或是建立自动同步关系
    * 各种己有同类平台开发团队
      * 通过沟通/协商,或是并入 docspot平台开发团队,或是建立API 接口关系,逐步形成联盟

日常活动::
  * 参考 [梦断代码 (豆瓣)](http://www.douban.com/subject/3142280/) 就知道,一个开放组织也得有固定的日常沟通活动,否则最容易停滞不前!
  * 建议形成最最最基础的制度先::
    * 所有成员订阅统一的列表,进行日常沟通
    * 每周在固定时间进行 IRC 快速实时沟通,确认进度


### 计划 ###
孕育期::
  * 目标:探索和完善出有自个儿特色的在线图书撰写工程思想的平台!
  * 参考:如何组织在线图书工程
    * http://code.google.com/p/openbookproject/wiki/HowToBuildBookOnline
    * 在线技术图书的撰写不是简单的段落到段落就好的,是种复杂的再创造过程;
    * 多个段落的顺序调整
    * 原版图书的内容更新
    * 译者的发挥,再创作
    * 图片/图表/思维图谱的嵌入
    * 等等在线图书工程的基础问题没有完美解决前,是无法成功的吸引足够多的人参与的!
  * 步骤:
    * 低调发布平台
    * 聚集有闲有能力的人,形成团队
    * 收集高价值图书工程并完成之,形成核心内容吸引力
    * 在图书工程组织过程中,整理出有突破性的友好功能,完善进来

培育期::
  * 目标:在实战中实用化平台
  * 步骤:
    * 进一步吸引或是邀请不同类型的图书工程进驻
    * 针对不同团队的反馈,进一步总结出平台实用化需要加强的功能,并完善之
    * 形成完整的在线图书工程理念,撰写对应的实例或是文档
      * 丰富帮助文档,针对不同受众提供不同文档
      * 使用手册
      * 图书工程指南
      * API说明
      * ...
    * 和多个社区建立合作关系,建立内容镜像关系,形成:
      * docspot.org 是权威的内容撰写平台
      * 而其内容是可以快速友好的分享在各个空间中!
        * 可以修订模板或是编译脚本,在每个页脚追加许可,以及 docspot.org 的链接,积累品牌效益


养成期::
  * 目标:成规模发布平台/内容,建立网络形象
  * 步骤:
    * 统筹好各种媒体平台资源,统一大规模发布平台以及内容
    * 提供友好的反馈渠道,配置专人或是机器人来回答FAQ
    * 比如:
      * 在 zeuux.com 建立专区 使用在线聊天功能进行支持
      * 使用 zeuux.com 的日历API,形成图书工程协调平台...


运营期::
  * 目标:开始挖掘内容价值,落地实体媒体,形成利益反馈
  * 步骤:
    * 和出版社合作,以社区为法人进行出版
    * 同 CSDN 等等合作,成为内容供应商
    * 同 原生技术社区合作,成为中文翻译代理...


## Discuss ##
[发布一个Python的协同文档翻译平台 - OpenBookProject | Google 网上论坛](http://groups.google.com/group/openbookproject/browse_thread/thread/b77936bf675c23e8#) `引发深入讨论`

### 在线翻译vs版本管理 ###
```
> 关于
> + 但是在线翻译模式应该追加透过版本系统的离线模式:
>  - 不会 SVN/Hg/Git 等等版本系统的普遍人,使用在线正式进行贡献
>  - 有项目体验的,通过版本系统提交文件来进行贡献,并自然形成版本(而不是DB中的)
> 这一点，我记得以前似乎就因为有人喜欢Web方式，有人喜欢透过版本系统直接分成了2派，各自翻译相同的东西。
>
> 而且在一个平台上实现上Web方式和版本系统方式共存也很难实现，
> 因为翻译后的文本一个是透过Web直接存入数据库的，一个是普通的文本文件，很难将两者的翻译结果有效的合并。
>
```
这是一定有方法的,而且,当前DB为主的文档管理正式会造成最终图书发布环境的DB依赖也不是最好的数据管理方式;
  * 没有数据一致性的保证
  * 和 Sphinx 实例形式相差太远

至少有几个融合的方向:
```
1. DB为主:
 + 每个修订自动输出成文件并检入SVN中;
 + 使用SVN的用户不直接检入生产仓库,而是分支,再次通过DB后才可以检入自动编译用的生产仓库;
 好处是对当前系统变更小,而且SVN的冲突管理也令高级用户可以及时获得更新,进行主动修订;
 问题是原版图书文件升级后,无法方便的汇入DB;
2. SVN为主:
 + SVN用户的修订直接驱动编译脚本生成最终页面
 + 页面用户的修订通过DB合并成文件后,检入SVN 从而完成编译
 好处是版本是自然和绝对的,吻合高级用户习惯;也容易升级原版内容,或是追加新图书;
 问题是两种用户的内容同步复杂;需要修订代码...
3. 只用SVN:
 + 自动编译通过 SVN HOOKS 驱动,一但有正确检入就自动编译对应图书;
 + 网页用户实际操作文件,而不是DB字段
 好处是数据统一和简单以及标准化了!
 问题是段落的分析和处理也必须文件化,需要修订代码...
```

我(jinhao7773@gmail.com)昨晚想了一下，主要有以下几个难点：
  * 1、Web方式是以段落为单位进行翻译的提交，而SVN方式是以文件为单位提交。
  * 2、不仅要保证Web方式和SVN方式提交过去的翻译保持同步和防止冲突，而且还要与英文原版之间建立某种联系，以便及时发现更新，同步翻译。

另外关于Web方式和SVN方式，我觉得从面向的翻译者人群来考虑，因为这是相对比较专业的文档翻译，所以对于翻译者来说，能够使用SVN进行翻译提交应该是一个很基本的能力要求。
而且，使用svn方式，可以使用自己熟悉的编辑器，这对于REST文档格式正确的保证是有很多好处。
不过，我觉得当前主要的问题并不是采用哪种方式进行翻译或是技术实现上的问题，即使以前已经在使用的纯SVN方式其实可以说是已经很不错了。

主要的问题在于：
  * 1、翻译者的参与积极性，目前Python在国内的开发人数还是小众，其中愿意长期，稳定地抽出时间来进行翻译工作的人也是少之又少。
  * 2、翻译进程的持续性，由于文档和书籍是两种不同的形式，文档的特点是会保持更新，而目前组织的翻译项目，基本都没有考虑如何与英文文档保持同步，而是直接从某个时间点开始，签出英文文档，在这基础上进行翻译，翻译完成后就不再更新。
  * 3、翻译者之间的协调和交流，相互激励，像Web方式的，虽然可以通过评注使用户之间可以进行某种程度的交流，但是这种方式有效性还有待商榷。而以前的SVN方式更像是一次豪华的聚会，开始积极性很高，但是随着翻译的结束，就很少再去考虑如何将翻译成果展示给更多有这个阅读需要的人。


基于以上原因::
我觉得作为翻译平台，考虑的更多的应该是：
  * 1、为翻译者之间提供自动化的协调工作：比如任务的领取，翻译术语同步，进度的相互督促，以及其中的各种问题交流，另外非常重要的一点：在原文档有更新时，应该有一种很好的方式提醒相关责任者进行相应更新。
  * 2、如何最大程度的提高，保持翻译者的参与积极性，这是个和国内IT环境相关的问题，大家平时就很忙了，难得有休息时间也会有其他自己的事要做。


所以归根结底，**问题是如何有效的组织，运作一个翻译团队。**
因此，我觉得翻译平台可以从以下几点考虑：
  * 1、只使用SVN方式进行翻译的提交，以Web方式提供翻译者之间的协调，进度控制，以及与英文文档的同步问题，以及与阅读者之间的问题反馈。
  * 2、建立某种“永久性”的文档维护者机制，比如某个人专门负责Django 文档中 Model 那部分相关的文档翻译，维护，更新工作。这样既使翻译内容在一定程度上保持一致，也利于翻译的可持续发展。
  * 3、翻译平台提供文档的自动编译，当通过SVN提交翻译后，使阅读者可以最快的见到翻译成果。
  * 4、与其他社区，出版者进行合作，为翻译者的无私奉献提供一定程度的回报。



## 后续讨论 ##
一个项目或是社区想吸引到人，
在中国，仅仅理念是不行的，只有积累到一定的内容和高人后，才有权威吸引力！
所以，现阶段，真的是应该优化功能，加入翻译工程概念；
以及，哲思社区的后续发展支持結合，
所谓积厚薄发，
只要坚持，总能成功的！

  * (xuecan@gmail.com)：扩展能处理的格式：
有许多文档还不是基于 Sphinx 的，还有不少项目采用 LaTeX、docbook 或者其它方案编写文档。比如，wxWidgets
的文档（OT：我准备八月份开始来填这个挖了好几年的坑）采用 Oxygen 编译，用于生成手册的文档源文件仅存在于 trunk 中(在
tags 中从未看到这部分文件)，不管是不是 API  参考，全部以 .h 的形式存在，这个系统是否有良好的可扩展机制来实现这些？

  * （jinhao7773@gmail.com）回复：
只要是基于文本的文档总能找到合适的方法对他们进行良好的分段，就像项目文档中写的那样，只需要写对应的 file\_handler ，系统会自动找到并调用。
这个系统主要的目的是翻译人写的文档，不适合翻译API文档，因为API通常是有工具从源代码自动分析得来的，翻译API就相当于要翻译每个源代码文件了。
不知道 wxWidgets 的文档是不是就是这里： http://svn.wxwidgets.org/viewvc/wx/wxWidgets/trunk/docs/ ，这里的很多txt文件应该就是人写的文档了，很明显，这些文档和rest的形式很像，所以也很容易分段并重组，至于文档的编译，虽然可能做不到自动编译，但是至少肯定可以将数据库中的翻译后文档导出成和原文档一样的目录结构，然后进行手动编译。

  * (xuecan@gmail.com)： 完善授权许可（authz）机制：
这是想要能够很好的组织和管理的基础。加入 OpenID 的支持只不过是丰富了 authn 的手段，但是要在 QA 上有所保证，完善的 authz 机制应该是必要的。不能仅仅靠吸引更多的眼球来保证品质。
  * （jinhao7773@gmail.com）回复：
就像在发布的源代码中看到的一样，这个项目是作为dajngo app的形式组织的，所以authz并不是本项目考虑的重点，当然可能出于用户权限管理的需要，最后另外单独做一个app来专门进行这方面的处理更合适。


  * (xuecan@gmail.com)： 定制更适合中文特性的样式 及 定制更适合中文特性的插件
举个简单的例子，斜体在中文中其实很无厘头的事情。假设正文使用的是宋体样式的话，大多数英文中适用斜体的情况都适合使用类似楷体或者仿宋的字体替代。类似的还有类似符合中文习惯的
text-indent 等样式。

reST 书写大段英文可以方便的使用多行，对于英文来说自动将换行替换为空白字符是正确而有意义的，对中文则不是这样。我不了解是否已有类似的模块可以处理这件事，在行末使用“\”不是很方便，使用编辑器的
word-wrap 在中英混排的段落有时很难看。类似的舶来架构不能很好的适合国情的情况应该还有一些，是否均能够有效处理？

  * （jinhao7773@gmail.com）回复：
这个字体和样式的问题或许可以通过在输出成HTML时，为中文版本另外写一套CSS样式进行解决，
中文的手动换行与英文的确在最后生成文档是有区别的，但是可以通过如在逗号，句号处进行手动换行，减少这种差别带来的影响。

  * (xuecan@gmail.com)：在实用性上进一步做文章
全局的以及项目领域内的共享词库？标点符号的半角/全角自动检查？提供 XML-RPC
或类似接口以便可以使用桌面程序进行工作？当系统真正强大，关注的人和参与的人肯定会增加的。

  * （jinhao7773@gmail.com）回复：
对于全局或项目的共享专业术语的功能得有，不然翻译的结果会显得非常不统一。
至于其他统功能扩展方面那是很长远的事了。

＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

实际上，我（jinhao7773@gmail.com）觉得作为一个翻译平台来说，最后可能碰到的最大难题是没有多少人愿意稳定，长期地参与翻译(Python本来就小众，再要符合有时间，有志愿，有能力进行翻译这些条件的人更是少之又少了。)，毕竟这是一个相当花时间和精力，而且可以说是对自己没有直接回报的事。
对于很多人来说，有空余时间不如自己写些小程序或学习新技术来得实在。
另外，尤其是《Python核心编程》那样的事发生之后，我想很多人对于志愿翻译这样的事都还应该怀有一种心有余悸的心情。

想到这里，我觉得其实不如组织翻译一些更入门，更简单的东西来得实际，因为通常有中文阅读需求的人，是为了更快的对Python这个语言或相关项目进行入门或有个基本的了解，而对于需要深入了解其中技术细节的人来说，英文阅读是必备的技能，否则，在这条路上也不可能走的更远。

为什么Ruby在国内发展的势头比Python猛？很大程度上就是中文入门资料匮乏，版本落后的原因的造成的。直到现在Django的第一本书才出版，Python的书也基本只有那本《Python核心编程》可以说是质量和版本都跟上了。这与ROR的书籍形成了鲜明的对比。

所以，我觉得这个翻译平台所面向阅读者，应该是没有或只有较少Python基础，但是对这方面知识有兴趣的用户。
该平台的目标是致力于“推广和普及”Python在国内的发展，专门面向初级读者。

其实，要说Python的入门资料，已经翻译的很好的也不是没有，比如前几天刚刚有人发布了的 PyMOTW 1.4 中文版。

但是很遗憾的是，这些资料只发布了PDF版本，而且或许也仅仅在这个邮件列表上发布了。

我觉得对于这些资料发布，首先，提供一个可供在线浏览的HTML版本是绝对必须的，因为这可以让搜索引擎索引到，被用户搜索到，用户想看一可以直接在线浏览，否则实在太对不起翻译者的辛苦劳动了。

第二，或许Python用户都学到了Python社区低调务实的作风，而不像ROR社区那样会炒作，宣传，但是这对于Python的普及是非常不利的。