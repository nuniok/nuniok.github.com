---
title: Git操作场景化实践
date: 2018-03-04
tags: git
id: 1
---

小明（是一个虚构人物）作为一名开发工程师（认真脸），平时经常用 Git 提交代码，觉得有些操作姿势还是很不舒服的，于是专门研究了一下各种场景下如果操作更优雅。

简短的提供思路式的讲解。


## git merge 场景

### 场景一：分支 merge

有时候开发一个稍微大一些的需求持续个几天，搞一个分支去提交吧，于是有了 `git checkout -b mywork`，在 mywork 分支 commit C4、C5，然后主分支被 commit C3，最后我要将分支 merge 到之分支之上 `git merge mywork`。

![](/resource/img/15182443948597.jpg)

流程示意图如上面，使用 merge 的好处就是多人维护一个项目仓库的时候，要任何时候保证主分支代码是可用的，任何人不应该直接在 master 上提交代码。

### 场景二：merge request

fork \ merge request

![](/resource/img/15182456532437.jpg)



## 场景三：rebase

开发了很久，各种fix提交记录，终于测通过了，要合到主分支了。发现这么多无效信息的提交记录干扰我们阅读，这时可以通过rebase将你的多次提交记录压缩成一个commit信息，然后再合到主分支上。

![](/resource/img/15182459869424.jpg)

![](/resource/img/15184903464515.jpg)

压缩 commit
`git log` 选择你提交的前一个版本

`git rebase -i e9a13ba5adcc154d5717b107d55f416e61c03958`

然后对其中的各项 commit 选择 pick / f / drop

遇到问题后处理，然后 `git rebase --continue` 直到合并完成

rebase到最新提交前

把所有分支的提交记录都弄下来 `git fetch --all`

然后 `git rebase base/master`

还是遇到问题后处理，然后 `git rebase --continue` 直到合并完成

最后 `git push -f origin master`

还有处理过程中不想处理了可以 `git rebase --abort`


## blame

咨询（检举）谁写的代码为什么这么设计（写了一堆坑）。

`git blame __init__.py` 可以查看每行代码提交记录

![](/resource/img/15184912683256.jpg)


## grep

`git grep -n tensorflow` 可以根据关键字搜索代码

[7.5 Git 工具 - 搜索](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E6%90%9C%E7%B4%A2)

![](/resource/img/15201547049654.jpg)


## revert 

`git revert C2` revert 是将你的一次提交代码反向重新创建一个新的记录

![](/resource/img/15201551398904.jpg)


## patch

patch 的做法是将我们多次的提交diff成一个问题件，然后在 apply 作为一个新的 commit 提交。对于上面 rebase 那种多次提交并带着merge记录的很难通过rebase操作，patch会很方便的解决。

https://www.cnblogs.com/y041039/articles/2411600.html

![](/resource/img/15201577453732.jpg)


## hooks

git操作的一些钩子，可以帮你做一些检查。

https://git-scm.com/book/zh/v1/%E8%87%AA%E5%AE%9A%E4%B9%89-Git-Git%E6%8C%82%E9%92%A9

## stash

临时保存操作内容

保存记录 `git stash`
提取记录 `git stash pop`

https://git-scm.com/book/zh/v1/%E8%87%AA%E5%AE%9A%E4%B9%89-Git-Git%E6%8C%82%E9%92%A9


## cherry-pick

对已经提交的数据再次提交使用

1. 找到一个 commit，记录 log 值
2. 新建一个分支 `git checkout -b newbranch`
3. 将一个commit 复制到新分支提交一个新 commit。`git cherry-pick 38361a55138140827b31b72f8bbfd88b3705d77a` 

