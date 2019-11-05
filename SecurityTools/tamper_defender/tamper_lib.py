#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3
from hashlib import md5
import os
import time
from socket import gethostname
from SecurityTools.tamper_defender import tamper_sender


def file_to_dir(file):
    return "/".join(file.split('/')[0:-1])


class GetData(object):
    def __init__(self, path, exclude_path, exclude_file):
        self.path = path
        self.exclude_path = exclude_path
        self.exclude_file = exclude_file

    # 递归遍历目录下的文件
    def get_file_path(self):
        file_path_list = []
        for root, dirs, files in os.walk(self.path):
            if root not in self.exclude_path:
                for name in files:
                    path_file = os.path.join(root, name)
                    if path_file not in self.exclude_file:
                        if path_file.__contains__('.swp'):
                            pass
                        else:
                            file_path_list.append(path_file)
                    else:
                        continue
            else:
                continue
        return file_path_list

    # 递归遍历目录下的目录
    def get_dir_path(self):
        dir_path_list = []
        for root, dirs, files in os.walk(self.path):
            if root not in self.exclude_path:
                dir_path_list.append(root)
            else:
                continue
        return dir_path_list


    # 获取md5字典
    def get_md5_dict(self):
        d = {}
        for filepath in self.get_file_path():
            file_size = 100 * 1024 * 1024
            file_content = open(filepath, 'rb')
            m = md5()
            while True:
                file_slice = file_content.read(file_size)
                if not file_slice:
                    break
                m.update(file_slice)
            md5str = m.hexdigest()
            file_content.close()
            md5str = str(md5str).lower()
            d.update({filepath: md5str})
        return d


class FileOperation(object):
    def __init__(self, path, root):
        self.path = path
        self.root = root

    # 初始文件备份
    def files_backup(self):
        os.system("\cp -f %s %s%s" % (self.path, self.root, self.path))

    # 备份文件还原
    def recover_file(self):
        s = os.system("\cp -f %s%s %s" % (self.root, self.path, self.path))
        return s

    def delete_file(self):
        s = os.system("rm -rf %s" % self.path)
        return s


class FileCompare(object):
    def __init__(self, dict_old, dict_new):
        self.dict_old = dict_old
        self.dict_new = dict_new

    def operation_list(self):
        missing_set = set([])
        illegal_set = set([])
        modified_set = set([])
        for key in self.dict_old.keys():
            if key not in self.dict_new.keys():
                missing_set.add(key)
        for key in self.dict_new.keys():
            if key not in self.dict_old.keys():
                illegal_set.add(key)
        for key in self.dict_new.keys():
            if key in self.dict_old.keys():
                if self.dict_old[key] == self.dict_new[key]:
                    continue
                else:
                    modified_set.add(key)
        return missing_set, illegal_set, modified_set


class TamperOperation(object):
    def __init__(self, err_file, log_root, backup_root):
        self.err_file = err_file
        self.sub_msg1 = "入侵警告"
        self.sub_msg2 = "温馨提示"
        self.sub_msg3 = "恢复失败告警"
        self.localtime = time.asctime(time.localtime(time.time()))
        self.hostname = gethostname()
        self.log_root = log_root
        self.backup_root = backup_root

    def file_missing(self):
        intrusion_msg = self.localtime + "--------" + "主机" + self.hostname + "被篡改了！" + self.err_file + "    丢失！"
        os.system("echo '%s' >> %s/alert.log" % (intrusion_msg, self.log_root))
        tamper_sender.mail_sender(intrusion_msg, self.sub_msg1)
        if not os.path.exists(file_to_dir(self.err_file)):
            os.system("mkdir -p %s" % file_to_dir(self.err_file))
        else:
            pass
        operation = FileOperation(self.err_file, self.backup_root)
        status_code = operation.recover_file()
        if status_code == 0:
            operation_msg = self.localtime + "--------" + "主机" + self.hostname + "执行恢复操作：" + self.err_file + "    已恢复!"
            os.system("echo '%s' >> %s/alert.log" % (operation_msg, self.log_root))
            tamper_sender.mail_sender(operation_msg, self.sub_msg2)
        else:
            operation_msg = self.localtime + "--------" + "主机" + self.hostname + "执行恢复操作：" + self.err_file + "    恢复失败!"
            os.system("echo '%s' >> %s/alert.log" % (operation_msg, self.log_root))
            tamper_sender.mail_sender(operation_msg, self.sub_msg3)

    def file_illegal(self):
        intrusion_msg = self.localtime + "--------" + "主机" + self.hostname + "被篡改了！" + self.err_file + "    非法创建！"
        os.system("echo '%s' >> %s/alert.log" % (intrusion_msg, self.log_root))
        tamper_sender.mail_sender(intrusion_msg, self.sub_msg1)
        operation = FileOperation(self.err_file, self.backup_root)
        status_code = operation.delete_file()
        if status_code == 0:
            operation_msg = self.localtime + "--------" + "主机" + self.hostname + "执行恢复操作：" + self.err_file + "    已删除!"
            os.system("echo '%s' >> %s/alert.log" % (operation_msg, self.log_root))
            tamper_sender.mail_sender(operation_msg, self.sub_msg2)
        else:
            operation_msg = self.localtime + "--------" + "主机" + self.hostname + "执行恢复操作：" + self.err_file + "    删除失败!"
            os.system("echo '%s' >> %s/alert.log" % (operation_msg, self.log_root))
            tamper_sender.mail_sender(operation_msg, self.sub_msg3)

    def file_modified(self):
        intrusion_msg = self.localtime + "--------" + "主机" + self.hostname + "被篡改了！" + self.err_file + "    被改动！"
        os.system("echo '%s' >> %s/alert.log" % (intrusion_msg, self.log_root))
        tamper_sender.mail_sender(intrusion_msg, self.sub_msg1)
        operation = FileOperation(self.err_file, self.backup_root)
        status_code = operation.recover_file()
        if status_code == 0:
            operation_msg = self.localtime + "--------" + "主机" + self.hostname + "执行恢复操作：" + self.err_file + "    已恢复!"
            os.system("echo '%s' >> %s/alert.log" % (operation_msg, self.log_root))
            tamper_sender.mail_sender(operation_msg, self.sub_msg2)
        else:
            operation_msg = self.localtime + "--------" + "主机" + self.hostname + "执行恢复操作：" + self.err_file + "    恢复失败!"
            os.system("echo '%s' >> %s/alert.log" % (operation_msg, self.log_root))
            tamper_sender.mail_sender(operation_msg, self.sub_msg3)

    def dir_missing(self):
        intrusion_msg = self.localtime + "--------" + "主机" + self.hostname + "被篡改了！" + '文件夹' + self.err_file + "    非法创建！"
        os.system("echo '%s' >> %s/alert.log" % (intrusion_msg, self.log_root))
        tamper_sender.mail_sender(intrusion_msg, self.sub_msg1)
        operation = FileOperation(self.illegal_dir, self.backup_root)
        status_code = operation.delete_file()
        if status_code == 0:
            operation_msg = self.localtime + "--------" + "主机" + self.hostname + "执行恢复操作：" + '文件夹' + self.err_file + "    已删除!"
            os.system("echo '%s' >> %s/alert.log" % (operation_msg, self.log_root))
            tamper_sender.mail_sender(operation_msg, self.sub_msg2)
        else:
            operation_msg = self.localtime + "--------" + "主机" + self.hostname + "执行恢复操作：" + '文件夹' + self.err_file + "    删除失败!"
            os.system("echo '%s' >> %s/alert.log" % (operation_msg, self.log_root))
            tamper_sender.mail_sender(operation_msg, self.sub_msg3)
