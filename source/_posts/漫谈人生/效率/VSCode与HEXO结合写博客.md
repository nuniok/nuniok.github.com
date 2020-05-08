---
title: VS Code 与 HEXO 结合写博客
date: 2020-04-05
tags: [vscode, hexo]
id: 3
---

在 mac 机器上可以使用 mweb 来写博客，比较好用的地方就是可以直接把剪贴板的图片粘贴上来，缺点是 mac 键盘超难用并且不支持窗口内开启命令行。平时在家的时候都用 Ubuntu 台式机，博客使用 VS Code 编写，一直以来阻挡我的是图片的粘贴特别费劲，今天发现一个很好用的插件 pasteimage，可以直接将剪贴板图片粘贴到 markdown 使用，并且支持配置保存路径。

![](/resource/img/2020-04-05-15-57-27.png)

然后按照教程配置好参数：

```
{
    "pasteImage.path": "${projectRoot}/source/resource/img",
    "pasteImage.basePath": "${projectRoot}/source",
    "pasteImage.forceUnixStyleSeparator": true,
    "pasteImage.prefix": "/"
}
```

就可以直接将图片粘贴到 markdown 中，其中遇到个问题就是配置不生效，会导致文件直接保存到当前文件目录，具体配置方法可以参考下面连接。

> https://www.crifan.com/vscode_how_to_config_setting_plugin/  这篇文章写的很详细了。
> https://github.com/mushanshitiancai/vscode-paste-image 这篇是配置教程，里面有些地方比较容易被误导。

对于Linux系统需要有 xclip 支持，使用的时候会给提示的。

![](/resource/img/2020-04-05-16-03-56.png)

另外记录一下 Ubuntu 的截屏和粘贴快捷键：

```
Ctrl + Shift + Print Screen  // 区域截屏到剪贴板
Ctrl + Alt + s  // 在 VS Code 中粘贴
```