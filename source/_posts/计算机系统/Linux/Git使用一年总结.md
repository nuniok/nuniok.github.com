---
title: Git使用一年总结
date: 2015-08-14
tags: Git
id: 1
---

##### git fetch merge
```
git remote -vv
git remote add base git@git.in.xxx.com:sss/xxx.git
git fetch base
git merge base/master
```

##### git切换远程仓库地址
```
git remote set-url origin [url]
```

##### 使用git在本地创建一个项目的过程
```
$ makdir ~/hello-world    //创建一个项目hello-world
$ cd ~/hello-world       //打开这个项目
$ git init             //初始化
$ touch README
$ git add README        //更新README文件
$ git commit -m 'first commit'     //提交更新，并注释信息“first commit”
$ git remote add origin git@github.test/hellotest.git     //连接远程github项目
$ git push -u origin master     //将本地项目更新到github项目上去
```

---------------------

##### git设置关闭自动换行
`git config --global core.autocrlf false`
为了保证文件的换行符是以安全的方法，避免windows与unix的换行符混用的情况，最好也加上这么一句
`git config --global core.safecrlf true`

---------------------

##### git tag 使用
```
git tag  # 列出当前仓库的所有标签
git tag -l 'v0.1.*'  # 搜索符合当前模式的标签

git tag v0.2.1-light  # 创建轻量标签
git tag -a v0.2.1 -m '0.2.1版本'  # 创建附注标签

git checkout [tagname]  # 切换到标签
git show v0.2.1  # 查看标签版本信息

git tag -d v0.2.1  # 删除标签
git tag -a v0.2.1 9fbc3d0  # 补打标签

git push origin v0.1.2  # 将v0.1.2标签提交到git服务器
git push origin –tags  # 将本地所有标签一次性提交到git服务器
git tag  # 查看当前分支下的标签
```


-------------------

##### git pull问题
```
You asked me to pull without telling me which branch you
want to merge with, and 'branch.content_api_zhangxu.merge' in
your configuration file does not tell me, either. Please
specify which branch you want to use on the command line and
try again (e.g. 'git pull <repository> <refspec>').
See git-pull(1) for details.

If you often merge with the same branch, you may want to
use something like the following in your configuration file:

    [branch "content_api_zhangxu"]
    remote = <nickname>
    merge = <remote-ref>

    [remote "<nickname>"]
    url = <url>
    fetch = <refspec>

See git-config(1) for details.
```
`git pull origin new_branch`

----------------

##### 怎样遍历移除项目中的所有 .pyc 文件
`sudo find /tmp -name "*.pyc" | xargs rm -rf`替换`/tmp`目录为工作目录
`git rm *.pyc`这个用着也可以

避免再次误提交，在项目新建`.gitignore`文件，输入`*.pyc`过滤文件

-----------------

##### git变更项目地址
`git remote set-url origin git@192.168.6.70:res_dev_group/test.git`
`git remote -v`

-----------------

##### 查看某个文件的修改历史
`git log --pretty=oneline 文件名   # 显示修改历史`
`git show 356f6def9d3fb7f3b9032ff5aa4b9110d4cca87e  # 查看更改`

-----------------

##### git push 时报错 warning: push.default is unset
git_push.jpg
'matching' 参数是 Git 1.x 的默认行为，其意是如果你执行 git push 但没有指定分支，它将 push 所有你本地的分支到远程仓库中对应匹配的分支。而 Git 2.x 默认的是 simple，意味着执行 git push 没有指定分支时，只有当前分支会被 push 到你使用 git pull 获取的代码。
根据提示，修改git push的行为:
git config --global push.default matching
再次执行git push 得到解决。

-------------------

##### git submodule的使用拉子项目代码

开发过程中，经常会有一些通用的部分希望抽取出来做成一个公共库来提供给别的工程来使用，而公共代码库的版本管理是个麻烦的事情。今天无意中发现了git的`git submodule`命令，之前的问题迎刃而解了。
添加

为当前工程添加submodule，命令如下：

`git submodule add 仓库地址 路径`

其中，仓库地址是指子模块仓库地址，路径指将子模块放置在当前工程下的路径。
注意：路径不能以 / 结尾（会造成修改不生效）、不能是现有工程已有的目录（不能順利 Clone）

命令执行完成，会在当前工程根路径下生成一个名为“.gitmodules”的文件，其中记录了子模块的信息。添加完成以后，再将子模块所在的文件夹添加到工程中即可。
删除

submodule的删除稍微麻烦点：首先，要在“.gitmodules”文件中删除相应配置信息。然后，执行`git rm –cached`命令将子模块所在的文件从git中删除。
下载的工程带有submodule

当使用`git clone`下来的工程中带有submodule时，初始的时候，submodule的内容并不会自动下载下来的，此时，只需执行如下命令：

`git submodule update --init --recursive`

即可将子模块内容下载下来后工程才不会缺少相应的文件。

------------------
##### 一些错误
###### "pathspec 'branch' did not match any file(s) known to git."错误
```
git checkout master
git pull
git checkout new_branch
```

###### 使用git提交比较大的文件的时候可能会出现这个错误

error: RPC failed; result=22, HTTP code = 411
fatal: The remote end hung up unexpectedly
fatal: The remote end hung up unexpectedly
Everything up-to-date

这样的话首先改一下git的传输字节限制

git config http.postBuffer  524288000
然后这时候在传输或许会出现另一个错误

error: RPC failed; result=22, HTTP code = 413
fatal: The remote end hung up unexpectedly
fatal: The remote end hung up unexpectedly
Everything up-to-date

这两个错误看上去相似，一个是411，一个是413

下面这个错误添加一下密钥就可以了

首先key-keygen 生成密钥

然后把生成的密钥复制到git中自己的账号下的相应位置

git push ssh://192.168.64.250/eccp.git  branch


> 等待收集




------------------

##### git add文件取消
在git的一般使用中，如果发现错误的将不想提交的文件add进入index之后，想回退取消，则可以使用命令：`git reset HEAD <file>...`，同时git add完毕之后，git也会做相应的提示。
> http://blog.csdn.net/yaoming168/article/details/38777763

-------------------

##### git删除文件：
删除文件跟踪并且删除文件系统中的文件file1`git rm file1`
提交刚才的删除动作，之后git不再管理该文件`git commit`

删除文件跟踪但不删除文件系统中的文件file1`git rm --cached file1`
提交刚才的删除动作，之后git不再管理该文件。但是文件系统中还是有file1。`git commit`

-------------------

##### 版本回退
版本回退用于线上系统出现问题后恢复旧版本的操作。
回退到的版本`git reset --hard 248cba8e77231601d1189e3576dc096c8986ae51`
回退的是所有文件，如果后悔回退可以git pull就可以了。

-------------------

##### 历史版本对比
查看日志`git log`
查看某一历史版本的提交内容`git show  4ebd4bbc3ed321d01484a4ed206f18ce2ebde5ca`，这里能看到版本的详细修改代码。
对比不同版本`git diff c0f28a2ec490236caa13dec0e8ea826583b49b7a  2e476412c34a63b213b735e5a6d90cd05b014c33`
> http://blog.csdn.net/lxlzhn/article/details/9356473

-------------------

##### 分支的意义与管理
创建分支可以避免提交代码后对主分支的影响，同时也使你有了相对独立的开发环境。分支具有很重要的意义。
创建并切换分支，提交代码后才能在其它机器拉分支代码`git checkout -b new_branch`
查看当前分支`git branch`
切换到master分支`git checkout master`
合并分支到当前分支`git merge new_branch`，合并分支的操作是从new_branch合并到master分支，当前环境在master分支。
删除分支`git branch -d new_branch`

--------------------

##### git冲突文件编辑
冲突文件冲突的地方如下面这样
```
a123
<<<<<<< HEAD
b789
=======
b45678910
>>>>>>> 6853e5ff961e684d3a6c02d4d06183b5ff330dcc
c
```
冲突标记<<<<<<< （7个<）与=======之间的内容是我的修改，=======与>>>>>>>之间的内容是别人的修改。
此时，还没有任何其它垃圾文件产生。
你需要把代码合并好后重新走一遍代码提交流程就好了。

---------------------

##### 不顺利的代码提交流程
在`git push`后出现错误可能是因为其他人提交了代码，而使你的本地代码库版本不是最新。
这时你需要先`git pull`代码后，检查是否有文件冲突。
没有文件冲突的话需要重新走一遍代码提交流程`add —> commit —> push`。
解决文件冲突在后面说。

---------------------

##### git顺利的提交代码流程
查看修改的文件`git status`；
为了谨慎检查一下代码`git diff`；
添加修改的文件`git add dirname1/filename1.py dirname2/filenam2.py`，新加的文件也是直接add就好了；
添加修改的日志`git commit -m "fixed:修改了上传文件的逻辑"`；
提交代码`git push`，如果提交失败的可能原因是本地代码库版本不是最新。

----------------------

##### 理解github的pull request
###### 有一个仓库，叫Repo A。你如果要往里贡献代码，首先要Fork这个Repo，于是在你的Github账号下有了一个Repo A2,。然后你在这个A2下工作，Commit，push等。然后你希望原始仓库Repo A合并你的工作，你可以在Github上发起一个Pull Request，意思是请求Repo A的所有者从你的A2合并分支。如果被审核通过并正式合并，这样你就为项目A做贡献了。
> http://zhidao.baidu.com/question/1669154493305991627.html

----------------------

##### 创建和使用git ssh key
首先设置git的user name和email：
```
git config --global user.name "xxx"
git config --global user.email "xxx@gmail.com"
```
查看git配置：
```
git config --list
```
###### 然后生成SHH密匙：
查看是否已经有了ssh密钥：`cd ~/.ssh`
如果没有密钥则不会有此文件夹，有则备份删除
生存密钥：
```
ssh-keygen -t rsa -C "gudujianjsk@gmail.com"
```
按3个回车，密码为空这里一般不使用密钥。
最后得到了两个文件：id_rsa和id_rsa.pub
注意：密匙生成就不要改了，如果已经生成到`~/.ssh`文件夹下去找。


```
// 暂时无用
添加 私密钥 到ssh：ssh-add id_rsa
需要之前输入密码（如果有）。

在github上添加ssh密钥，这要添加的是“id_rsa.pub”里面的公钥。
打开 http://github.com,登陆xushichao，然后添加ssh。
注意在这里由于直接复制粘帖公钥，可能会导致增加一些字符或者减少些字符，最好用系统工具xclip来做这些事情。
xclip -selection c  id_rsa.pub
```

> 应用流程未整理

---------------------------

###### 网络上收集
```
master : 默认开发分支； origin : 默认远程版本库

初始化操作
    $ git config -global user.name <name>  #设置提交者名字
    $ git config -global user.email <email>  #设置提交者邮箱
    $ git config -global core.editor <editor>  #设置默认文本编辑器
    $ git config -global merge.tool <tool>  #设置解决合并冲突时差异分析工具
    $ git config -list  #检查已有的配置信息

创建新版本库
    $ git clone <url>  #克隆远程版本库
    $ git init  #初始化本地版本库

修改和提交
    $ git add .  #添加所有改动过的文件
    $ git add <file>  #添加指定的文件
    $ git mv <old> <new> #文件重命名
    $ git rm <file>  #删除文件
    $ git rm -cached <file>  #停止跟踪文件但不删除
    $ git commit -m <file> #提交指定文件
    $ git commit -m “commit message”  #提交所有更新过的文件
    $ git commit -amend  #修改最后一次提交
    $ git commit -C HEAD -a -amend  #增补提交（不会产生新的提交历史纪录）

查看提交历史
    $ git log  #查看提交历史
    $ git log -p <file>  #查看指定文件的提交历史
    $ git blame <file>  #以列表方式查看指定文件的提交历史
    $ gitk  #查看当前分支历史纪录
    $ gitk <branch> #查看某分支历史纪录
    $ gitk --all  #查看所有分支历史纪录
    $ git branch -v  #每个分支最后的提交
    $ git status  #查看当前状态
    $ git diff  #查看变更内容

撤消操作
    $ git reset -hard HEAD  #撤消工作目录中所有未提交文件的修改内容
    $ git checkout HEAD <file1> <file2>  #撤消指定的未提交文件的修改内容
    $ git checkout HEAD. #撤消所有文件
    $ git revert <commit>  #撤消指定的提交

分支与标签
    $ git branch  #显示所有本地分支
    $ git checkout <branch/tagname>  #切换到指定分支或标签
    $ git branch <new-branch>  #创建新分支
    $ git branch -d <branch>  #删除本地分支
    $ git tag  #列出所有本地标签
    $ git tag <tagname>  #基于最新提交创建标签
    $ git tag -d <tagname>  #删除标签

合并与衍合
    $ git merge <branch>  #合并指定分支到当前分支
    $ git rebase <branch>  #衍合指定分支到当前分支

远程操作
    $ git remote -v  #查看远程版本库信息
    $ git remote show <remote>  #查看指定远程版本库信息
    $ git remote add <remote> <url>  #添加远程版本库
    $ git fetch <remote>  #从远程库获取代码
    $ git pull <remote> <branch>  #下载代码及快速合并
    $ git push <remote> <branch>  #上传代码及快速合并
    $ git push <remote> : <branch>/<tagname>  #删除远程分支或标签
    $ git push -tags  #上传所有标签
```
