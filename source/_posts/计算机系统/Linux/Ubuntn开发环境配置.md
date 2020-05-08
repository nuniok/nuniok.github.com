---
title: Ubuntu开发环境配置
date: 2017-11-22
tags: Ubuntu
id: 1
---

此博客记录为备份命令：


## Node 安装配置

不要使用 apt-get 带的版本，太旧，自己去官网下载安装，方法如下：

下载并解压 node-v6.9.5-linux-x64.tar.xz

`tar -xJf node-v6.9.5-linux-x64.tar.xz`

移到通用的软件安装目录 /opt/

`sudo mv node-v6.9.5-linux-x64 /opt/`

安装 npm 和 node 命令到系统命令

`sudo ln -s /opt/node-v6.9.5-linux-x64/bin/node /usr/local/bin/node`

`sudo ln -s /opt/node-v6.9.5-linux-x64/bin/npm /usr/local/bin/npm`

验证：

`node -v`


## ipython notebook 远程访问

创建配置

`ipython profile create common`

生成访问密码
```
In [1]: from notebook.auth import passwd
In [2]: passwd()
Enter password:
Verify password:
Out[2]: 'sha1:ce23d945972f:34769685a7ccd3d08c84a18c63968a41f1140274'
```

生成证书
`openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout common.pem -out common.pem`


在profile目录下, 编辑ipython_notebook_config.py

```
~/.ipython/profile_common/ipython_notebook_config.py
c = get_config()
c.NotebookApp.certfile=u'/home/xyz/.ipython/profile_common/common.pem'
c.NotebookApp.ip='*'
c.NotebookApp.open_browser=False
c.NotebookApp.password=u'sha1:c5f8fbcb1f9a:bfa8a1879fc2f6bd932a1a4089cbc9775cdcd98e'
c.NotebookApp.port=1234
```

启动命令

`ipython notebook --config=/home/xyz/.ipython/profile_common/ipython_notebook_config.py`


## 修改目录权限

`sudo chmod -R 775 .`


## Tensorflow GPU 运行环境安装

显卡驱动

```
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update
sudo apt-get install nvidia-384
```

CUDA 驱动安装

`sudo ./cuda_8.0.61_375.26_linux.run`

其中第一个显卡驱动选项不要再安装了

CUDNN 安装

```
tar -xzvf cudnn-8.0-linux-x64-v6.0.tgz
cd cudnn-8.0-linux-x64-v6.0/
sudo cp lib* /usr/local/cuda/lib64/
sudo cp cudnn.h /usr/local/cuda/include/
```

添加环境变量

```
export PATH=/usr/local/cuda-8.0/bin:$PATH
export PATH=/usr/local/cuda-8.0/lib64:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64:$LD_LIBRARY_PATH
```


## 查看 NVIDIA 显卡状态

`watch -n 1 -d nvidia-smi`