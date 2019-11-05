#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from SecurityTools.tamper_defender import tamper_config, tamper_lib


def main():
    # 原始文件备份
    if not os.path.exists(backup_root):
        os.system("mkdir -p %s" % backup_root)
        for path in path_list:
            path_data = tamper_lib.GetData(path, exclude_path, exclude_file)
            for dir_path in path_data.get_dir_path():
                os.system("mkdir -p %s%s" % (backup_root, dir_path))
            for file_path in path_data.get_file_path():
                file_data = tamper_lib.FileOperation(file_path, backup_root)
                file_data.files_backup()
    else:
        # 当不存在MD5字典时，创建MD5字典
        if os.path.exists("%s/md5_db.log" % log_root) == False:
            for path in path_list:
                data = tamper_lib.GetData(path, exclude_path, exclude_file)
                md5_dict = data.get_md5_dict()
            with open("%s/md5_db.log" % log_root, 'a') as f:
                f.write(str(md5_dict))
                f.close()
            for path in path_list:
                data = tamper_lib.GetData(path, exclude_path, exclude_file)
                dir_list = data.get_dir_path()
            with open("%s/dir_path.log" % log_root, 'a') as f:
                f.write(str(dir_list))
                f.close()
        else:
            for path in path_list:
                data = tamper_lib.GetData(path, exclude_path, exclude_file)
                md5_dict = data.get_md5_dict()
            d_new = md5_dict
            f = open("%s/md5_db.log" % log_root, 'r')
            d_old = eval(f.read())
            f.close()
            fc = tamper_lib.FileCompare(d_old, d_new)
            if (d_old == d_new) is False:
                fc_set = fc.operation_list()[0]
                if not fc_set:
                    pass
                else:
                    for err_file in fc_set:
                        tamper = tamper_lib.TamperOperation(err_file, log_root, backup_root)
                        tamper.file_missing()
                fc_set = fc.operation_list()[1]
                if not fc_set:
                    pass
                else:
                    for err_file in fc_set:
                        tamper = tamper_lib.TamperOperation(err_file, log_root, backup_root)
                        tamper.file_illegal()
                fc_set = fc.operation_list()[2]
                if not fc_set:
                    pass
                else:
                    for err_file in fc_set:
                        tamper = tamper_lib.TamperOperation(err_file, log_root, backup_root)
                        tamper.file_modified()
            else:
                f = open("%s/dir_path.log" % log_root, 'r')
                old_dir = eval(f.read())
                for path in path_list:
                    data = tamper_lib.GetData(path, exclude_path, exclude_file)
                    for illegal_dir in data.get_dir_path():
                        if illegal_dir not in old_dir:
                            tamper = tamper_lib.TamperOperation(illegal_dir, log_root, backup_root)
                            tamper.dir_mingssing()
                        else:
                            pass


if __name__ == '__main__':
    while True:
        path_list = tamper_config.path_list
        exclude_path = tamper_config.exclude_path
        exclude_file = tamper_config.exclude_file
        backup_root = tamper_config.backup_root
        log_root = tamper_config.log_root
        md5_value_list = []
        main()
