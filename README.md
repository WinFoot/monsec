monsec 企业安全月报系统
=========

    记录每月的安全漏洞、安全事件的信息和关键安全系统，针对中小企业安全人力有限可以直接部署使用，通过报表形式展现方便量化工作。

演示程序
---------

    (http://monsec.0zu.net)

使用说明
---------

    # 在当前目录下，自动安装Flask虚拟环境
    ./setup.py

    # 初始化数据库
    ./db_create.py

    # 运行程序
    ./run.py

    # 访问界面
    http://localhost:5000

兼容性
---------

    开发环境是CentOS6.0，系统默认python2.6

    如果运行中出现问题，请在github反馈。(https://github.com/anjkz/monsec/issues)

```
    # Ubuntu 在安装时报错，需要创建一个软连接
    # The "No module named _sysconfigdata_nd" is a bug in the Ubuntu package.

    $ sudo ln -s /usr/lib/python2.7/plat-*/_sysconfigdata_nd.py /usr/lib/python2.7/
```

截图
---------
![alt tag](https://raw.githubusercontent.com/anjkz/monsec/master/img.png)
