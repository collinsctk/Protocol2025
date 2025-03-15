#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import ftplib
import os
import sys
from pathlib import Path

# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
current_file = Path(__file__)
current_dir = current_file.parent


def putfile(hostname, file, username='anonymous', password='1@2.net', rdir='.', ldir='.', verbose=True):
    if verbose:
        print('上传文件:', file)
    os.chdir(ldir)  # 切换本地工作目录
    local = open(file, 'rb')  # 读取本地文件
    remote = ftplib.FTP(hostname)  # 连接站点
    remote.encoding = 'GB18030'  # 使用中文编码
    remote.login(username, password)  # 输入用户名和密码进行登录
    remote.cwd(rdir)  # 切换FTP目录
    
    # 提取文件名，不使用完整路径
    filename = os.path.basename(file)
    remote.storbinary('STOR ' + filename, local, 1024)  # 上传文件，只使用文件名
    
    remote.quit()  # 退出会话
    local.close()  # 关闭本地文件
    if verbose:
        print('上传文件:' + file + ' 结束！')


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    putfile('196.21.5.189',
            f'{current_dir}/ftp_get.py',
            'administrator',
            'Cisc0123',
            rdir='/qytang1/')  # 使用默认目录
