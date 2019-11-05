#!/bin/bash
pid_num=$(ps -ef | grep  tamper_main.py |grep -v grep| awk -F " " '{print $2}')
if [ -z ${pid_num} ];then
    nohup python36 tamper_main.py > /usr/local/tamper_defender/nohup.out 2>&1 &
    echo -e "/033[33mDone./033[0m"
else
    echo -e "The tamper_defender \033[31mis already protecting\033[0m your system and services!"
fi
