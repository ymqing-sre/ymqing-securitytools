#!/bin/bash
pid_num=$(ps -ef | grep  tamper_main.py |grep -v grep| awk -F " " '{print $2}')
if [ -z ${pid_num} ];then
    echo -e "There is \033[31mNO PROCESS\033[0m for tamper_defender!"
else
    kill -9 $pid_num
fi
echo "Backing project files up..."
sleep 1
rm -rf /usr/local/tamper_defender/backup_bak
mv /usr/local/tamper_defender/backup /usr/local/tamper_defender/backup_bak
echo "Cleaning residual files..."
sleep 1
rm -rf /usr/local/tamper_defender/md5_db.log
rm -rf /usr/local/tamper_defender/dir_path.log
echo -e "/033[33mDone./033[0m"