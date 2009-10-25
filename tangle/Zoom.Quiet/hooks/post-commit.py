#!/usr/local/bin/python
#coding=utf-8
"""
自动SVN HOOKs 事务处理支持
    - self.f = open( self.LOGFILE, "wa+") 尝试？！
    重新回到 "a+"
    - 指定新log 名 matter-ci.log
"""## Zoomq::060110 fixed log exp.
## Zoomq::060112 class matter agent
import sys,os,time
## Zoomq::060121 for t2t 处理
import popen2

class post_matter:
    """svn hooks post-commit matter agent
    """
    
    def __init__(self,log):
        """init agent usage sys env
            - matter 事务处理桟
                ,"chk":[path,umark]
                }
            ,]
        """
        # hooks 中没有环境变量都要显示的声明！
        self.T2T = "/usr/local/bin/txt2tags"
        # "/data1/www/blog.woodpecker/PyBlosxom/plugins/preformatters/txt2tags"
        #/usr/local/bin/
        self.CHMOD = "/bin/chmod"
        self.CHOWN = "/usr/sbin/chown"
        self.LOOK = "/usr/local/bin/svnlook"
        self.SVN = "/usr/local/bin/svn"
        daylog = "%s-%s.log"%(log[:-4]
                            ,time.strftime("%y%m%d",
                                            time.localtime()))
        self.LOGFILE = daylog
        #log
        #self.f = open( self.LOGFILE, "a+" )   
        # 如果没有就创建，进行追加内容     
        self.f = open( self.LOGFILE, "a+")
        #os.open( self.LOGFILE, os.O_CREAT | os.O_APPEND)
        self.TSTAMP = "%s"%time.strftime("%y-%m-%d %H:%M:%S", time.localtime())
        self.matter = []
    
    
    def __repr__(self):
        """自打印声明 帮助信息
        """
        return " post_matter agent Usage: " + sys.argv[0] + " REPOS REV\n"
    
    def usage(self):
        """使用性说明
        """
        print self
        print >> self.f,self.TSTAMP+" post_matter Usage::"+sys.argv[0]+" REPOS REV"
        sys.exit(0)
    
    def changed(self,rev,repos):
        """使用 svnlook 得到修改的路径
        """
        dirs = os.popen( self.LOOK+" changed -r "+ rev + " " + repos)
        return dirs
    
    def changedirs(self,rev,repos):
        """使用 svnlook 得到修改的路径
        """
        dirs = os.popen( self.LOOK+" changed -r "+ rev + " " + repos).read().strip()
        return dirs
    
    def changedirli(self,rev,repos):
        """使用 svnlook 得到修改的路径 list
        
        """
        dirs = os.popen( self.LOOK+" changed -r "+ rev + " " + repos).readlines()
        return dirs
    
    
    def chkdirmod(self,path,umark):
        """chmod and chown the aim path...
        """
        exp = os.popen(self.CHMOD+" -R "+umark+" "+path).read().strip()
        exp += os.popen(self.CHOWN+" -R www:www "+path).read().strip()
        print >> self.f,exp
        return exp
    def logcommit(self,rev,repos):
        """log commit info...
        """
        log = os.popen( self.LOOK+" author -r "+ rev + " " + repos).read().strip()
        print >> self.f," "*4+"%s commited;"%str(log)
    
    
    def addmatter(self,rev,repos,mark,aim,mod,path="NULL",umark="NULL"):
        """追加hooks事务
        """
        self.matter.append({"up":[rev,repos,mark,aim,mod]
                ,"chk":[path,umark]
                })        
        #print self.matter
        
    
    def domatters(self):
        """逐一进行事务处理...
        """
        if 0==len(self.matter):
            print >> self.f,self.TSTAMP+"~"*7+"NULL matter"
        else:
            print >> self.f,self.TSTAMP+"::"*7+"::%s SVN hook matter doing..."%len(self.matter)            
            for m in self.matter:
                #print >> self.f,self.TSTAMP+str(m)
                up = m["up"]
                ismark = self.autoco(up[0],up[1],up[2],up[3],up[4])
                chk = m["chk"]
                ## 直接忽略没有匹配的情况...
                if "NULL"==chk[0]:
                    pass
                elif 0==ismark:
                    ppath = chk[0][11:]
                    print >> self.f," "*7+"cancel dir::...%s"%ppath
                    pass
                    
                else:
                    self.chkdirmod(chk[0],chk[1])
                    
        UP = self.matter[0]["up"]
        self.logcommit(UP[0],UP[1])
        #self.chkpybt2t(self.changed(UP[0],UP[1])
        #               ,"pyblosxom/zoomquiet/data/")
        print >> self.f,self.TSTAMP+"::"*7+"::All matter done"
    
    
    
    def autoco(self,rev,repos,mark,aim,mod):
        """自动检出指定项目的代码到指定目录
            - rev  本次修改的版本
            - repos  本次修改的仓库
            - mark  匹配项
            - aim   输出目标
            - mod   检出的模块
           要求目标路径有预先检出的环境！
        """
        #dirs = self.changedirs(rev,repos)
        # 使用通用SVNLOOK 文件对象输出
        fdir = self.changed(rev,repos)    
        dirs = fdir.read().strip()   
        ismark = 0   
        if mark in dirs:
            ismark = 1
            print >> self.f,self.TSTAMP+" %s updating...>>>>marked::%s"%(("*"*7),mark)
            upsvn = "%s update %s"%(self.SVN,(aim+mod) )
            fup = os.popen(upsvn)
            up = fup.read().strip()
            print >> self.f,up         
            #self.chkdirt2t(dli,upli,"data")
            # 判别是否进行t2t 处理
            self.chkpybt2t(up
                            ,"pyblosxom/zoomquiet/data/")
            print >> self.f,self.TSTAMP+" updated All "+"*"*7
        else:
            #pass
            print >> self.f,self.TSTAMP+" %s up::nothing<<mark out::%s"%(("-"*7),mark)    
        #return fdir        
        print >> self.f," "*7+" ismark=%s"%ismark
        return ismark 
    
    
    
    
    
    
    def chkpybt2t(self,dirs,mark):
        """auto check PyBlosxom .t2t blog
        .......
            if os.path.isdir(self.param[1]):
            print >> self.f," %s ..uped...%s"%(mark
                                ,l.split()[-1])
        """
        #print >> self.f,"~"*7+"t2t::%s<<%s"%(dirs,len(dirs))
        for l in dirs.split():
            if mark in l:
                self.autot2t(l)
        #"""
        #return exp
    
    
    def autot2t(self,upath):
        """自动处理t2t 到对应PyBlosxom 目录
            - upath svnlook 出来的对应更新记录
            - t2t 文件本身输出 xhtml ，cp为txt 由PyBlosxom 显示
            - 另外输出为.moin 的wiki 文件
            --target moin
        """    
        #print >> self.f,"~"*7+"t2t::%s"%upath
        print >> self.f,"~"*7+"t2t::%s"%upath.split("/")[-1]
        #print >> self.f,"~"*7+"t2t::%s"%upath.split("/")[-1][:-4]
        t2txhtml = "%s %s"%(self.T2T,upath)
        cp2txt = "cp %s %s"%(upath[:-4]+".xhtml",upath[:-4]+".txt")
        t2tmoin = "%s %s %s"%(self.T2T," --target moin ",upath)
        print >> self.f,"~"*7+"t2t::%s"%t2txhtml
        #print >> self.f,"~"*7+"t2t::%s"%cp2txt
        #print >> self.f,"~"*7+"t2t::%s"%t2tmoin
        print >> self.f,"~"*7+"t2t::%s"%os.popen(t2txhtml)
        #done = os.popen(t2txhtml)
        #print >> self.f,"~"*7+"t2t::%s"%done.read().strip()
        #os.popen(cp2txt)
        #os.popen(t2tmoin)
        try:
            r, w, e = popen2.popen3(t2txhtml)
            #print >> self.f,"~"*7+"t2t::%s"%r.read()
            print >> self.f,"~"*7+"t2t::%s"%e.read()
            #r, w, e = popen2.popen3(cp2txt)
            #print >> self.f,"~"*7+"t2t::%s"%r.read()
            #print >> self.f,"~"*7+"t2t::%s"%e.read()
            r, w, e = popen2.popen3(t2tmoin)
            #print >> self.f,"~"*7+"t2t::%s"%r.read()
            print >> self.f,"~"*7+"t2t::%s"%e.read()
            #e.readlines()
            #r.readlines()
            r.close()
            e.close()
            w.close()        
        except:
            print >> self.f,"~"*7+"t2t::popen2.popen3() ::crash"
        
        
        #return exp
        """06-01-21 14:27:24 ******* updating...>>>>marked::pyblosxom
    U    /data1/www/blog.woodpecker/pyblosxom/zoomquiet/ZqsPyBlosxom.leo
    U    /data1/www/blog.woodpecker/pyblosxom/zoomquiet/data/Mode/movie/060116-zenpoem.t2t
    Updated to revision 398.
    ~~~~~~~t2t::/data1/www/blog.woodpecker/pyblosxom/zoomquiet/data/Mode/movie/060116-zenpoem.t2t
        """
    
    
    


    
if __name__ == '__main__':
    """自省运行...
    """
    p = post_matter("/var/log/svn/ci4matter/matter-ci.log")
    if len(sys.argv) != 3:
        p.usage()
    # start hook matter...
    repos = sys.argv[1]
    rev = sys.argv[2]
    
    ## Python 产品事务
    ## 初始性事务:: matter SVN 自管理
    p.addmatter(rev,repos
        ,"data/svn/matter"
        ,"/data1/www/svn.woodpecker/repos/matter"
        ,"")
    p.addmatter(rev,repos
        ,"data/svn/matter/conf"
        ,"/data1/www/svn.woodpecker/repos/matter/conf"
        ,""
        ,"/data1/www/svn.woodpecker/repos/matter/conf/"
        ,"775")
    p.addmatter(rev,repos
        ,"data/svn/matter/hooks"
        ,"/data1/www/svn.woodpecker/repos/matter/hooks"
        ,""
        ,"/data1/www/svn.woodpecker/repos/matter/hooks/"
        ,"775")
    ## woodpecker SVN repo事务
    p.addmatter(rev,repos
        ,"data/svn/woodpecker/conf"
        ,"/data1/www/svn.woodpecker/repos/woodpecker/conf"
        ,""
        ,"/data1/www/svn.woodpecker/repos/woodpecker/conf/"
        ,"775")
    p.addmatter(rev,repos
        ,"data/svn/woodpecker/hooks"
        ,"/data1/www/svn.woodpecker/repos/woodpecker/hooks"
        ,""
        ,"/data1/www/svn.woodpecker/repos/woodpecker/hooks/"
        ,"775")
    ## kad.cn SVN repo事务
    """
    p.addmatter(rev,repos
        ,"data/svn/kad/conf"
        ,"/data1/www/svn.woodpecker/repos/kad/conf"
        ,""
        ,"/data1/www/svn.woodpecker/repos/kad/conf/"
        ,"775")
    p.addmatter(rev,repos
        ,"data/svn/kad/hooks"
        ,"/data1/www/svn.woodpecker/repos/kad/hooks"
        ,""
        ,"/data1/www/svn.woodpecker/repos/kad/hooks/"
        ,"775")
    """    #060528 追加trac0.10dec 的维护
    p.addmatter(rev,repos
        ,"trac/trac-environment"
        ,"/usr/local/lib/python2.4/site-packages/trac"
        ,""
        ,"/usr/local/lib/python2.4/site-packages/trac/"
        ,"775")
        
    p.addmatter(rev,repos
        ,"trac/conf"
        ,"/data1/www/svn.woodpecker/trac/conf"
        ,""
        ,"/data1/www/svn.woodpecker/trac/conf/"
        ,"775")
    
    ## MoinMoin事务
    ##zoomq::070709 updated for MoinMoin1.5.5a
    p.addmatter(rev,repos
        ,"wiki/MoinMoin"
        ,"/usr/local/lib/python2.4/site-packages/MoinMoin"
        ,""
        ,"/usr/local/lib/python2.4/site-packages/MoinMoin/"
        ,"775")
    
    p.addmatter(rev,repos
        ,"moin153/server"
        ,"/data1/www/wiki.woodpecker/moin/server"
        ,""
        ,"/data1/www/wiki.woodpecker/moin/server/"
        ,"775")
    p.addmatter(rev,repos
        ,"moin153/htdocs"
        ,"/data1/www/wiki.woodpecker/moin/htdocs"
        ,""
        ,"/data1/www/wiki.woodpecker/moin/htdocs/"
        ,"775")
    p.addmatter(rev,repos
        ,"moin153/data/plugin"
        ,"/data1/www/wiki.woodpecker/moin/data/plugin"
        ,""
        ,"/data1/www/wiki.woodpecker/moin/data/plugin/"
        ,"775")
    p.addmatter(rev,repos
        ,"moin153/config"
        ,"/data1/www/wiki.woodpecker/moin/config"
        ,""
        ,"/data1/www/wiki.woodpecker/moin/config/"
        ,"775")
    
    ## MoinMoin事务 for wiki.BillXu.com
    p.addmatter(rev,repos
        ,"billxu/server"
        ,"/data1/www/wiki.woodpecker/billxu/server"
        ,""
        ,"/data1/www/wiki.woodpecker/billxu/server/"
        ,"775")
    p.addmatter(rev,repos
        ,"billxu/data/plugin"
        ,"/data1/www/wiki.woodpecker/billxu/data/plugin"
        ,""
        ,"/data1/www/wiki.woodpecker/billxu/data/plugin/"
        ,"775")
    
    
    ## httpd事务
    p.addmatter(rev,repos
        ,"apache2/Includes"
        ,"/usr/local/etc/apache2/Includes/"
        ,""
        ,"/usr/local/etc/apache2/Includes/"
        ,"775")   
    ## lighttpd事务
    p.addmatter(rev,repos
        ,"usrloc/etc"
        ,"/usr/local/etc/"
        ,"")
    
    ## 因为 sudoers 必须有特殊权限绑定！
    #chkdirmod(CHMOD,CHOWN,"/usr/local/etc","775")    
    
    ## Blog事务::060116 追加支持PyBlosxom 的t2t自动分析
    ### Zoomq::060512-细分PyBlosxom 事务
    # 内容Entry更新
    p.addmatter(rev,repos
        ,"blog/pyblosxom/zoomquiet"
        ,"/data1/www/blog.woodpecker/pyblosxom/zoomquiet"
        ,""
        ,"/data1/www/blog.woodpecker/pyblosxom/zoomquiet/"
        ,"777")
        
    # PyBlosxom 1.3.0b更新
    p.addmatter(rev,repos
        ,"blog/pyblosxom/Pyblosxom-1.3.0b"
        ,"/data1/www/blog.woodpecker/pyblosxom/Pyblosxom-1.3.0b"
        ,""
        ,"/data1/www/blog.woodpecker/pyblosxom/Pyblosxom-1.3.0b/"
        ,"775")
    # PyBlosxom 1.3.2更新
    p.addmatter(rev,repos
        ,"blog/pyblosxom/Pyblosxom-1.3.2"
        ,"/data1/www/blog.woodpecker/pyblosxom/Pyblosxom-1.3.2"
        ,""
        ,"/data1/www/blog.woodpecker/pyblosxom/Pyblosxom-1.3.2/"
        ,"775")
    # flavours更新
    p.addmatter(rev,repos
        ,"blog/pyblosxom/flavours"
        ,"/data1/www/blog.woodpecker/pyblosxom/flavours"
        ,""
        ,"/data1/www/blog.woodpecker/pyblosxom/flavours/"
        ,"775")
    
    # plugins更新
    p.addmatter(rev,repos
        ,"blog/pyblosxom/plugins"
        ,"/data1/www/blog.woodpecker/pyblosxom/plugins"
        ,""
        ,"/data1/www/blog.woodpecker/pyblosxom/plugins/"
        ,"775")
    
    ## Blog事务::060124 追加Planet的管理
    p.addmatter(rev,repos
        ,"blog/planet"
        ,"/data1/www/blog.woodpecker/planet"
        ,""
        ,"/data1/www/blog.woodpecker/planet/"
        ,"775")
    
    
    
    
    ## WeKnow事务
    p.addmatter(rev,repos
        ,"weknow/TiddlyWiki"
        ,"/data1/www/weknow.woodpecker/TiddlyWiki"
        ,""
        ,"/data1/www/weknow.woodpecker/TiddlyWiki/"
        ,"775")
    
    ## demo 体验事务
    p.addmatter(rev,repos
        ,"demo"
        ,"/data1/www/demo.woodpecker"
        ,""
        ,"/data1/www/demo.woodpecker/"
        ,"775")
    ## 060604:: ZoomQuiet.org 首页
    
    p.addmatter(rev,repos
        ,"www/zqidx"
        ,"/data1/www/www.woodpecker/data/_stuff/zqidx"
        ,""
        ,"/data1/www/www.woodpecker/data/_stuff/zqidx/"
        ,"775")
    
    
    
    ## portal事务
    p.addmatter(rev,repos
        ,"idx"
        ,"/data1/www/www.woodpecker/data/idx"
        ,""
        ,"/data1/www/www.woodpecker/data/idx/"
        ,"775")
        
    
    
    ### at last do all reg hook matter
    p.domatters()    
    
    
    
    


