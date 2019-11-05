Release: SAO防篡改系统ver.1.1

ReleaseNote：
    1.修复了保护目录的下级目录必须要有文件而不能仅仅只有文件夹的BUG
    2.给启动脚本添加了进程检测，避免重复启动多个进程
    3.给启动/停止脚本添加了友情提示
    4.简化了主程序代码

功能简介:
    1.支持对文件、文件夹的新增、删除、修改邮件告警
    2.支持当检测到文件、文件夹的新增、删除、修改等篡改操作时的原始文件还原
    3.支持多防护目录配置
    4.支持多目录白名单设置、多文件白名单设置

安装配置:
    运行环境：
        Python3.6
        需要将python3.6的执行文件软连接到/usr/bin下：
        ln -s Python3.6安装目录/bin/python3 /usr/bin/python36

    执行文件配置：
        默认将tamper_defender.ver.1.tar.gz放置于/usr/local目录下再进行解压，生成tamper_defender文件夹。
        文件树如下：
        tamper_defender
        ├── start_defender.sh
        ├── stop_defender.sh
        ├── tamper_config.py
        ├── tamper_lib.so
        ├── tamper_main.py
        └── tamper_sender.so
        如需修改执行文件部署位置，需修改start_defender.sh及stop_defender.sh文件
        # vim start_defender.sh
        #!/bin/bash
        nohup python36 tamper_main.py > /usr/local/tamper_defender/nohup.out 2>&1 &

        # vim stop_defender.sh
        #!/bin/bash
        pid_num=$(ps -ef | grep  tamper_main.py |grep -v grep| awk -F " " '{print $2}')
        kill -9 $pid_num
        sleep 1
        rm -rf /usr/local/tamper_defender/backup_bak
        mv /usr/local/tamper_defender/backup /usr/local/tamper_defender/backup_bak
        sleep 1
        rm -rf /usr/local/tamper_defender/md5_db.log

        将两个脚本文件中/usr/local/tamper_defender修改为自定义tamper_defender解压路径

    参数配置：
        修改tamper_config.py中参数来设置被保护目录、白名单目录及文件、邮件发送地址等。
        [root@localhost tamper_defender]# vim tamper_config.py

        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        path_list = ["/tomcat8.2/webapps1", "/tomcat8.2/webapps2"]                                  # 这里填写需要监控的目录列表，使用英文逗号分隔
        exclude_path = ["/tomcat8.2/webapps1/subapp", "/tomcat8.2/webapps1/logs"]                   # 这里填写需要排除的目录，使用英文逗号分隔，若不需要设置请配置成exclude_path = []
        exclude_file = ["/tomcat8.2/webapps1/subapp/11.log", "/tomcat8.2/webapps1/subapp/22.log"]   # 这里填写需要排除的单个文件，使用英文逗号分隔，若不需要设置请配置成exclude_file = []
        backup_root = "/usr/local/tamper_defender/backup"                                           # 备份文件的根目录，千万不要提前手动创建！！！
        log_root = "/usr/local/tamper_defender"                                                     # 进程的日志目录，如不使用默认目录，需要手动创建！
        # 以下是发件邮箱及收件人信息，发现邮箱需要打开smtp服务
        mail_host = "smtp.189.cn"                                   # smtp地址，这里用的189邮箱
        mail_user = "*******"                                       # 邮箱登陆账户名
        mail_pass = "*******"                                       # 邮箱登陆密码
        sender = '189****4365@189.cn'                               # 真实发件地址
        receivers = ["*******@qq.com", "******@sina.com"]           # 收件人邮箱地址

程序执行：
    确保start_defender.sh及stop_defender.sh具备执行权限
    使用./start_defender.sh开启防护
    使用./stop_defender.sh关闭防护

    程序启动后文件树：
        tamper_defender
        ├── alert.log  # 文件篡改告警日志及恢复日志，文件被篡改后产生
        ├── backup     # 被保护文件的备份目录，程序启动后自动产生
        │   └── usr
        │       └── local
        │           └── tomcat8.2
        │               └── webapps3
        │                   └── notice
        │                       ├── css
        │                       │   ├── common-css.css
        │                       │   └── normalize.css
        │                       ├── images
        │                       │   └── logo.jpeg
        │                       └── index.html
        ├── mail.log   # 邮件提示发送日志，文件被篡改后产生
        ├── md5_db.log # 被保护文件的MD5字典
        ├── nohup.out  # 程序异常终止的报错日志
        ├── __pycache__
        │   └── tamper_config.cpython-36.pyc
        ├── start_defender.sh   # 程序启动脚本
        ├── stop_defender.sh    # 程序终止脚本
        ├── tamper_config.py    # 配置文件
        ├── tamper_lib.so
        ├── tamper_main.py      # 主进程
        └── tamper_sender.so

    程序正常停止后文件树：
        tamper_defender
        ├── alert.log
        ├── backup_bak  # 备份文件的备份
        │   └── usr
        │       └── local
        │           └── tomcat8.2
        │               └── webapps3
        │                   └── notice
        │                       ├── css
        │                       │   ├── common-css.css
        │                       │   └── normalize.css
        │                       ├── images
        │                       │   └── logo.jpeg
        │                       └── index.html
        ├── mail.log
        ├── nohup.out
        ├── __pycache__
        │   └── tamper_config.cpython-36.pyc
        ├── start_defender.sh
        ├── stop_defender.sh
        ├── tamper_config.py
        ├── tamper_lib.so
        ├── tamper_main.py
        └── tamper_sender.so

版本已知BUG（重要）：
    1.暂无

程序异常关闭处理：
    异常关闭定义：
        未通过stop_defender.sh进行的程序关闭均属于异常关闭。
    异常关闭特征：
        默认配置情况下，在tamper_defender程序主目录下会残留backup文件及md5_db.log，nohup.out中有输出报错信息。
    处理方式：
        不要执行start和stop脚本文件，通知开发人员进行处理


