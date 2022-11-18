#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from ftplib import FTP
import re
import optparse
import os
from tools.decorator_time import print_run_time


@print_run_time()
def ftp_find(hostname, username, password, start_dir='/', file_type='.py', verbose=True):
    if verbose:
        print('查找整个FTP中的特定文件(递归查询)，并且返回清单！')
    try:
        connection = FTP(hostname)  # 连接站点
        connection.encoding = 'GB18030'  # 使用中文编码
        connection.login(username, password)  # 输入用户名和密码进行登录
        path = []  # 所有文件的路径都将最终放入path清单

        def dir_recursive(dirpath):  # 定义目录递归查询的函数
            ls = []  # LIST命令执行的结果，放入ls清单
            connection.cwd(dirpath)  # 进入特定目录
            connection.retrlines('LIST', ls.append)  # 执行LIST命令，并且把结果添加到ls清单
            for line in ls:  # 逐行读取LIST命令返回结果
                # print(line)
                # 文件的格式
                # 04-30-16  10:34AM                  388 FTP_LIST.py
                # 目录的格式
                # 04-30-16  09:39AM       <DIR>          QYT
                patt = r'(\d\d-\d\d-\d\d)\s*(\d\d\:\d\d\w\w)\s*(<DIR>|\d*)\s*(\w.*)'  # 匹配命令返回结果的正则表达式
                scan_result = re.match(patt, line)  # 正则表达式匹配
                # date = scan_result.group(1)  # 第一个部分(\d\d-\d\d-\d\d)为日期
                # time = scan_result.group(2)  # 第二个部分(\d\d\:\d\d\w\w)为时间
                dir_or_length = scan_result.group(3)  # 第三个部分(<DIR>|\d*)目录或者文件大小
                dir_or_filename = scan_result.group(4)  # 第四个部分文件或者目录名

                if dir_or_length != '<DIR>':  # 如果不为目录，当然就是文件了
                    if dirpath == '/':  # 如果当前路径在‘/’根目录
                        path.append(dirpath + dir_or_filename)  # 把文件路径加入path清单
                    else:  # 如果当前路径不在‘/’根目录
                        path.append(dirpath + '/' + dir_or_filename)  # 把文件路径加入path清单
                else:  # 如果是目录
                    if dirpath == '/':  # 如果当前路径在‘/’根
                        dir_recursive(dirpath + dir_or_filename)  # 进行递归查询
                    else:  # 如果当前路径不在‘/’根目录
                        dir_recursive(dirpath + '/' + dir_or_filename)  # 进行递归查询

        dir_recursive(start_dir)  # 执行函数
        connection.close()  # 退出FTP连接会话
        filetype_in_ftp = []  # 最终返回的，特定类型文件的清单
        for x in path:  # 遍历整个文件清单
            if os.path.splitext(x)[1] == file_type:  # 如果后缀名与我们查找文件的后缀名相同
                filetype_in_ftp.append(x)  # 把找到的文件放入filetype_in_ftp清单

        return filetype_in_ftp  # 返回filetype_in_ftp清单
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    print(ftp_find('10.1.1.200', 'qytang', 'Cisc0123', '/', '.py'))
