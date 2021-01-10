#!/usr/bin/python
# -*- coding: utf-8 -*-
import pexpect
import logging
import logger as logger
import time


class GetNetworkConfig:

    # 通过telnet方式登录华为网络设备执行配置备份
    def huawei_telnet_getconfig(self,loginCMD,loginName,loginPassword,filename):
        #登录设备,spawn()方法用来执行登录命令
        child = pexpect.spawn(loginCMD)
        child.timeout = 5
        logging.debug('spawn loginCMD: %s' %loginCMD)
        #logFileId 返回结果保存在文件中
        logFileId = open(filename, 'wb')
        #logfile_read获取标准输出的内容,记录执行程序中返回的所有内容，也就是去掉你发出去的命令，而仅仅只包括命令结果的部分
        child.logfile_read = logFileId
        #logfile运行输出控制,既包含了程序运行时的输出，也包含了 spawn 向程序发送的内容
        # child.logfile = logFileId
        #模式匹配阀值, searchwindowsize 的值表示一次性收到多少个字符之后才匹配一次表达式
        child.searchwindowsize = 200
        #expect() - 关键字匹配,等待指定的关键字
        #它最后会返回 0 表示匹配到了所需的关键字，如果后面的匹配关键字是一个列表的话，
        # 就会返回一个数字表示匹配到了列表中第几个关键字，从 0 开始计算。
        #expect() 支持利用正则表达式来匹配所需的关键字
        login_result = child.expect(['Username:','Login:', pexpect.EOF, pexpect.TIMEOUT])
        logging.debug('login_result: %d' %login_result)
        if (login_result <=1 ):
            # 匹配'username','login'字符串成功，输入用户名.
            # sendline() - 发送带回车符的字符串
            child.sendline(loginName)
            logging.debug('sendline loginName: %s'  %loginName)
            passwd_result = child.expect(['Password:','password:',pexpect.EOF, pexpect.TIMEOUT])
            logging.debug('passwd_result: %d' %passwd_result)
            if passwd_result <=1:
                child.sendline(loginPassword)
                logging.debug('sendline loginPassword: %s' %loginPassword)
                #time.sleep(1)
                #cisco提示符 用户模式 >  特权模式  #
                #华为提示符  用户视图 >  特权模式   ]
                #linux提示符 用户模式 $  特权模式  #
                prompt_result = child.expect([">","]", pexpect.EOF, pexpect.TIMEOUT])
                logging.debug('prompt_result: %d'  %prompt_result)
                #如果匹配到">","]"这4种提示符，就发送任务命令
                if prompt_result <= 1:
                    #child.sendline(taskCMD)
                    child.sendline('sys')
                    time.sleep(0.2)
                    child.sendline('user-interface vty 0 4')
                    time.sleep(0.2)
                    child.sendline('screen-length 0')
                    time.sleep(0.2)
                    child.sendline('q')
                    time.sleep(0.2)
                    child.sendline('q')
                    time.sleep(0.2)
                    child.sendline('disp curr')
                    logging.debug('disp curr')
                    time.sleep(2)
                    child.sendline('sys')
                    time.sleep(0.2)
                    child.sendline('user-interface vty 0 4')
                    time.sleep(0.2)
                    child.sendline('screen-length 30')
                    time.sleep(0.2)
                    child.sendline('q')
                    time.sleep(0.2)
                    child.sendline('q')
                    time.sleep(0.2)
                    #time.sleep(1)
                    prompt = child.expect([pexpect.EOF, pexpect.TIMEOUT])
                    if prompt <=1 :
                        child.sendline('quit')
                else:
                    logging.debug("[---]输入密码后登录失败")
            else:
                logging.debug("[---] 输入账号后没返回Password输入标识符")
                child.close(force=True)
        logFileId.close()
        child.close()

    # 通过ssh方式登录华为网络设备执行配置备份
    def huawei_ssh_getconfig(self,loginCMD,loginPassword,filename):
        #登录设备,spawn()方法用来执行登录命令
        child = pexpect.spawn(loginCMD)
        child.timeout = 5
        #logFileId 返回结果保存在文件中
        logFileId = open(filename, 'wb')
        #logfile_read获取标准输出的内容,记录执行程序中返回的所有内容，也就是去掉你发出去的命令，而仅仅只包括命令结果的部分
        child.logfile_read = logFileId
        #logfile运行输出控制,既包含了程序运行时的输出，也包含了 spawn 向程序发送的内容
        # child.logfile = logFileId
        #模式匹配阀值, searchwindowsize 的值表示一次性收到多少个字符之后才匹配一次表达式
        child.searchwindowsize = 200
        #expect() - 关键字匹配,等待指定的关键字
        #它最后会返回 0 表示匹配到了所需的关键字，如果后面的匹配关键字是一个列表的话，
        # 就会返回一个数字表示匹配到了列表中第几个关键字，从 0 开始计算。
        #expect() 支持利用正则表达式来匹配所需的关键字
        passwd_result = child.expect(['Password:','password:',pexpect.EOF, pexpect.TIMEOUT])
        logging.debug('passwd_result: %d' %passwd_result)
        if passwd_result <= 1:
            child.sendline(loginPassword)
            logging.debug('sendline loginPassword: %s' %loginPassword)
            #time.sleep(1)
            #cisco提示符 用户模式 >  特权模式  #
            #华为提示符  用户视图 >  特权模式   ]
            #linux提示符 用户模式 $  特权模式  #
            prompt_result = child.expect([">","]", pexpect.EOF, pexpect.TIMEOUT])
            logging.debug('prompt_result: %d'  %prompt_result)
            #如果匹配到">","]"这4种提示符，就发送任务命令
            if prompt_result <= 1:
                child.sendline('sys')
                time.sleep(0.2)
                child.sendline('user-interface vty 0 4')
                time.sleep(0.2)
                child.sendline('screen-length 0')
                time.sleep(0.2)
                child.sendline('q')
                time.sleep(0.2)
                child.sendline('q')
                time.sleep(0.2)
                child.sendline('disp curr')
                logging.debug('disp curr')
                time.sleep(2)
                child.sendline('sys')
                time.sleep(0.2)
                child.sendline('user-interface vty 0 4')
                time.sleep(0.2)
                child.sendline('screen-length 30')
                time.sleep(0.2)
                child.sendline('q')
                time.sleep(0.2)
                child.sendline('q')
                time.sleep(0.2)
                prompt = child.expect([pexpect.EOF, pexpect.TIMEOUT])
                if prompt <=1 :
                    child.sendline('quit')
            else:
                logging.debug("[---]输入密码后登录失败")
        else:
            logging.debug("[---] 输入账号后没返回Password输入标识符")
            child.close(force=True)
        logFileId.close()
        child.close()

    # 通过telnet方式登录CISCO网络设备执行配置备份
    def cisco_telnet_getconfig(self,loginCMD,loginName,loginPassword,filename):
        #登录设备,spawn()方法用来执行登录命令
        child = pexpect.spawn(loginCMD)
        child.timeout=5
        logging.debug('spawn loginCMD: %s' %loginCMD)
        #模式匹配阀值, searchwindowsize 的值表示一次性收到多少个字符之后才匹配一次表达式
        # logFileId 返回结果保存在文件中
        logFileId = open(filename, 'wb')
        # logfile_read获取标准输出的内容,记录执行程序中返回的所有内容，也就是去掉你发出去的命令，而仅仅只包括命令结果的部分
        #child.logfile_read = logFileId
        # logfile运行输出控制,既包含了程序运行时的输出，也包含了 spawn 向程序发送的内容
        child.logfile = logFileId
        child.searchwindowsize = 200
        #expect() - 关键字匹配,等待指定的关键字
        #它最后会返回 0 表示匹配到了所需的关键字，如果后面的匹配关键字是一个列表的话，
        # 就会返回一个数字表示匹配到了列表中第几个关键字，从 0 开始计算。
        #expect() 支持利用正则表达式来匹配所需的关键字
        login_result = child.expect(['Username:','Login:', pexpect.EOF, pexpect.TIMEOUT])
        logging.debug('login_result: %d' %login_result)
        if (login_result <=1 ):
            # 匹配'username','login'字符串成功，输入用户名.
            # sendline() - 发送带回车符的字符串
            child.sendline(loginName)
            logging.debug('sendline loginName: %s'  %loginName)
            passwd_result = child.expect(['Password:','password:',pexpect.EOF, pexpect.TIMEOUT])
            logging.debug('passwd_result: %d' %passwd_result)
            if passwd_result <=1:
                child.sendline(loginPassword)
                logging.debug('sendline loginPassword: %s' %loginPassword)
                #cisco提示符 用户模式 >  特权模式  #
                #华为提示符  用户视图 >  特权模式   ]
                #linux提示符 用户模式 $  特权模式  #
                prompt_result = child.expect([">","#", pexpect.EOF, pexpect.TIMEOUT])
                logging.debug('prompt_result: %d'  %prompt_result)
                #如果匹配到">","]"这4种提示符，就发送任务命令
                if prompt_result <= 1 :
                    child.sendline('en')
                    time.sleep(0.2)
                    child.sendline('terminal length 0')
                    time.sleep(0.2)
                    child.sendline('show run')
                    logging.debug('show run')
                    time.sleep(2)
                    prompt = child.expect([pexpect.EOF, pexpect.TIMEOUT])
                    if prompt <=1 :
                        child.sendline('quit')
                        logging.debug('quit')
                else:
                    logging.debug('command terminal result : EOF or TIMEOUT')
            else:
                logging.debug("no password return")
        else:
            logging.debug("no username return")
        logging.debug('child close')
        logFileId.close()
        child.close()

    # 通过ssh方式登录DP网络设备执行配置备份
    def dp_ssh_getconfig(self,loginCMD,loginPassword,filename):
        #登录设备,spawn()方法用来执行登录命令
        child = pexpect.spawn(loginCMD)
        child.timeout=5
        logging.debug('spawn loginCMD: %s' %loginCMD)
        #模式匹配阀值, searchwindowsize 的值表示一次性收到多少个字符之后才匹配一次表达式
        # logFileId 返回结果保存在文件中
        logFileId = open(filename, 'wb')
        # logfile_read获取标准输出的内容,记录执行程序中返回的所有内容，也就是去掉你发出去的命令，而仅仅只包括命令结果的部分
        #child.logfile_read = logFileId
        # logfile运行输出控制,既包含了程序运行时的输出，也包含了 spawn 向程序发送的内容
        child.logfile = logFileId
        child.searchwindowsize = 200
        #expect() - 关键字匹配,等待指定的关键字
        #它最后会返回 0 表示匹配到了所需的关键字，如果后面的匹配关键字是一个列表的话，
        # 就会返回一个数字表示匹配到了列表中第几个关键字，从 0 开始计算。
        #expect() 支持利用正则表达式来匹配所需的关键字
        login_result = child.expect(['Password:','password:', pexpect.EOF, pexpect.TIMEOUT])
        logging.debug('login_result: %d' %login_result)
        if (login_result <=1 ):
            # 匹配'username','login'字符串成功，输入用户名.
            # sendline() - 发送带回车符的字符串
            child.sendline(loginPassword)
            logging.debug('sendline loginPassword: %s' %loginPassword)
            #cisco提示符 用户模式 >  特权模式  #
            #华为提示符  用户视图 >  特权模式   ]
            #linux提示符 用户模式 $  特权模式  #
            prompt_result = child.expect([">","#", pexpect.EOF, pexpect.TIMEOUT])
            logging.debug('prompt_result: %d'  %prompt_result)
            #如果匹配到">","]"这4种提示符，就发送任务命令
            if prompt_result <= 1 :
                child.sendline('terminal line 0')
                time.sleep(0.2)
                child.sendline('show run')
                logging.debug('show run')
                time.sleep(2)
                prompt = child.expect([pexpect.EOF, pexpect.TIMEOUT])
                if prompt <=1 :
                    child.sendline('exit')
                    logging.debug('exit')
            else:
                logging.debug('command terminal result : EOF or TIMEOUT')
        else:
            logging.debug("no password return")
        logging.debug('child close')
        logFileId.close()
        child.close()

    # 通过ssh方式登录JUNIPER SSG550M 网络设备执行配置备份
    def juniper_ssh_getconfig(self,loginCMD,loginPassword,filename):
        #登录设备,spawn()方法用来执行登录命令
        child = pexpect.spawn(loginCMD)
        child.timeout=5
        logging.debug('spawn loginCMD: %s' %loginCMD)
        #模式匹配阀值, searchwindowsize 的值表示一次性收到多少个字符之后才匹配一次表达式
        # logFileId 返回结果保存在文件中
        logFileId = open(filename, 'wb')
        # logfile_read获取标准输出的内容,记录执行程序中返回的所有内容，也就是去掉你发出去的命令，而仅仅只包括命令结果的部分
        #child.logfile_read = logFileId
        # logfile运行输出控制,既包含了程序运行时的输出，也包含了 spawn 向程序发送的内容
        child.logfile = logFileId
        child.searchwindowsize = 200
        #expect() - 关键字匹配,等待指定的关键字
        #它最后会返回 0 表示匹配到了所需的关键字，如果后面的匹配关键字是一个列表的话，
        # 就会返回一个数字表示匹配到了列表中第几个关键字，从 0 开始计算。
        #expect() 支持利用正则表达式来匹配所需的关键字
        login_result = child.expect(['Password:','password:', pexpect.EOF, pexpect.TIMEOUT])
        logging.debug('login_result: %d' %login_result)
        if (login_result <=1 ):
            # 匹配'username','login'字符串成功，输入用户名.
            # sendline() - 发送带回车符的字符串
            child.sendline(loginPassword)
            logging.debug('sendline loginPassword: %s' %loginPassword)
            #cisco提示符 用户模式 >  特权模式  #
            #华为提示符  用户视图 >  特权模式   ]
            #linux提示符 用户模式 $  特权模式  #
            prompt_result = child.expect([">","#", pexpect.EOF, pexpect.TIMEOUT])
            logging.debug('prompt_result: %d'  %prompt_result)
            #如果匹配到">","]"这4种提示符，就发送任务命令
            if prompt_result <= 1 :
                child.sendline('set console page 0')
                time.sleep(0.2)
                child.sendline('get config')
                time.sleep(2)
                prompt = child.expect([pexpect.EOF, pexpect.TIMEOUT])
                if prompt <=1 :
                    child.sendline('exit')
            else:
                logging.debug('command terminal result : EOF or TIMEOUT')
        else:
            logging.debug("no password return")
        logging.debug('child close')
        logFileId.close()
        child.close()

    # 当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；
    # 当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。


if __name__ == "__main__":
    mylogger = logger.Logger()
    # logging.debug('this is a debug from Logger.py')
    s=GetNetworkConfig()
    s.huawei_telnet_getconfig("telnet 10.222.5.1", "ywpt", "HBLTcisco*()", "huawei_telnet_10.222.5.1.log")
    s.huawei_ssh_getconfig("ssh ywpt@10.222.0.235","HBLTcisco*()","huawei_ssh_10.222.0.235.log")
    s.cisco_telnet_getconfig("telnet 10.222.0.206","ywpt","HBLTcisco*()","cisco_telnet_result.log")
    s.dp_ssh_getconfig("ssh ywpt@10.222.0.244","HBLTcisco*()","dp_ssh_10.222.0.244.log")
    s.juniper_ssh_getconfig("ssh ywpt@10.222.0.240","HBLTcisco*()","dp_ssh_10.222.0.240.log")

''' index = p.expect(['good', 'bad', pexpect.EOF, pexpect.TIMEOUT])
    if index == 0:
        do_something()
    elif index == 1:
        do_something_else()
    elif index == 2:
        do_some_other_thing()
    elif index == 3:
        do_something_completely_different()

cisco提示符：
用户模式>   特权模式#

华为提示符：
 用户视图>  特权模式]
 
linux提示符：
用户模式$  特权模式#

华为交换机不分页显示
>user-interface vty 0 4
>screen-length 0
默认screen-length 24

思科路由器/交换机
1. 在特权模式下键入“ terminal length 0”以将您的终端设置为无间断显示。
2.键入“ show run”或“ show start”以显示适用的配置。配置将显示，没有任何中断或暂停。

Cisco ASA防火墙上:
在特权模式下键入“ pager 0”以将您的终端设置为无间断显示。
2.键入“ show run-config”以显示配置。
'''



