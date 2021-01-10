#!/usr/bin/python
# coding=utf-8
import logger as logger
import logging
import os
from datetime import datetime

from readconfig import ReadConfig
from configbackup import GetNetworkConfig

cf = ReadConfig('config.ini')
# 获取备份目录
backupdir = cf.get('backup_dir','backupdir')
# 获取IP地址(存储成列表)
network_huawei_telnet_ip = cf.get('network_huawei_telnet', 'network_huawei_ip').split(',')
network_huawei_ssh_ip = cf.get('network_huawei_ssh', 'network_huawei_ip').split(',')
network_cisco_telnet_ip = cf.get('network_cisco_telnet', 'network_cisco_ip').split(',')
network_dp_ssh_ip = cf.get('network_dp_ssh', 'network_dp_ip').split(',')
network_juniper_ssh_ip = cf.get('network_juniper_ssh', 'network_juniper_ip').split(',')
# 获取用户
network_user = cf.get('network_user','network_user')
# 获取密码
network_password = cf.get('network_user','network_password')


if __name__ == '__main__':
    mylogger = logger.Logger()
    s = GetNetworkConfig()
    # 获取当天日期
    now=datetime.now()
    today = datetime.strftime(now, '%Y%m%d')

    for huawei_ip in network_huawei_telnet_ip:
        logging.debug('-------Begin : ' + huawei_ip +'--------')
        login_cmd = "telnet "+huawei_ip.strip()
        config_file = backupdir+"/"+today+"_"+huawei_ip.strip()+"_config.txt"
        s.huawei_telnet_getconfig(login_cmd,network_user,network_password,config_file)
        logging.error('Success Backup!'+config_file)

    for huawei_ip in network_huawei_ssh_ip:
        logging.debug('-------Begin : ' + huawei_ip + '--------')
        login_cmd = "ssh ywpt@"+huawei_ip.strip()
        config_file = backupdir+"/"+today+"_"+huawei_ip.strip()+"_config.txt"
        s.huawei_ssh_getconfig(login_cmd,network_password,config_file)
        logging.error('Success Backup!'+config_file)

    for cisco_ip in network_cisco_telnet_ip:
        logging.debug('-------Begin : ' + cisco_ip + '--------')
        login_cmd = "telnet "+cisco_ip.strip()
        config_file = backupdir+"/"+today+"_"+cisco_ip.strip()+"_config.txt"
        s.cisco_telnet_getconfig(login_cmd,network_user,network_password,config_file)
        logging.error('Success Backup!'+config_file)

    for dp_ip in network_dp_ssh_ip:
        logging.debug('-------Begin : ' + dp_ip + '--------')
        login_cmd = "ssh ywpt@"+dp_ip.strip()
        config_file = backupdir+"/"+today+"_"+dp_ip.strip()+"_config.txt"
        s.dp_ssh_getconfig(login_cmd,network_password,config_file)
        logging.error('Success Backup!'+config_file)

    for juniper_ip in network_juniper_ssh_ip:
        logging.debug('-------Begin : ' + juniper_ip + '--------')
        login_cmd = "ssh ywpt@" + juniper_ip.strip()
        config_file = backupdir + "/" + today + "_" + juniper_ip.strip() + "_config.txt"
        s.juniper_ssh_getconfig(login_cmd, network_password, config_file)
        logging.error('Success Backup!' + config_file)