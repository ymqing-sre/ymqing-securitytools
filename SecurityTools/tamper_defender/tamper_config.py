#!/usr/bin/env python
# -*- coding: utf-8 -*-
path_list = ["/usr/local/tomcat8.2/webapps2/scjzfp", "/usr/local/tomcat8.2/webapps3/notice"]  # 这里填写需要监控的目录列表
exclude_path = ["/home"]  # 这里填写需要排除的目录
exclude_file = ["/home/11.log"]  # 这里填写需要排除的单个文件
backup_root = "/usr/local/tamper_defender/backup"  # 备份文件的根目录
log_root = "/usr/local/tamper_defender"

mail_host = "smtp.189.cn"
mail_user = "18982074365"
mail_pass = "jamesyee890208"
sender = '18982074365@189.cn'
receivers = ["850643702@qq.com"]
