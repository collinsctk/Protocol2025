#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import poplib
import re
import email
import base64
from email.header import decode_header, make_header

attachment_dir = './attachment_dir/'


def decode_subject_base64(need_decode_str):
    # # 解码如下内容
    # # =?utf-8?b?6ZmE5Lu25rWL6K+VX+S4u+mimA==?=
    # #   utf-8   6ZmE5Lu25rWL6K+VX+S4u+mimA== (转码后为:附件测试_主题)
    # try:
    #     re_result = re.match(r'=\?(.*)\?\w\?(.*)\?=', need_decode_str).groups()
    #     # re_result[0] 为编码方式
    #     middle = re_result[1]  # 提取base64的内容 6ZmE5Lu25rWL6K+VX+S4u+mimA==
    #     decoded = base64.b64decode(middle)  # 对内容进行base64解码
    #     decoded_str = decoded.decode(re_result[0])  # 再对base64解码后内容,进行utf-8解码,转换为中文内容
    # except Exception:
    #     decoded_str = need_decode_str
    # return decoded_str

    return str(make_header(decode_header(need_decode_str)))


def qyt_rec_mail(mailserver, mailuser, mailpasswd, save_file=False, delete_email=False):
    print('Connecting...')
    server = poplib.POP3_SSL(mailserver, 995)  # 连接到邮件服务器
    server.user(mailuser)  # 邮件服务器用户名
    server.pass_(mailpasswd)  # 邮件服务器密码
    mails_list = []
    try:
        print(server.getwelcome())  # 打印服务器欢迎信息
        # b'+OK QQMail POP3 Server v1.0 Service Ready(QQMail v2.0)'
        msg_count, msg_bytes = server.stat()  # 查询邮件数量与字节数
        print('There are', msg_count, 'mail message in', msg_bytes, 'bytes')  # 打印邮件数量与字节数
        # There are 2 mail message in 153385 bytes
        server_list_result = server.list()
        print(server_list_result)  # 打印邮件清单
        # (b'+OK', [b'1 76634', b'2 76751'], 18)
        msg_count = len(server_list_result[1])

        for email_no in range(msg_count):  # 逐个读取邮件range(10) = 0 - 9
            hdr, message, octets = server.retr(email_no + 1)  # 读取邮件
            str_message = email.message_from_bytes(b'\n'.join(message))  # 把邮件内容拼接到大字符串
            part_list = []
            mail_dict = {}
            # walk() 能找到邮件的多个部分
            for part in str_message.walk():  # 把邮件的多个部分添加到part_list
                part_list.append(part)

            # 把邮件的第一个[0]部分内容提取出来写入字典mail_dict
            # 注意第一部分,所有邮件都会存在,是邮件的头部信息
            for header_name, header_content in part_list[0].items():
                if header_name == 'Subject':
                    mail_dict[header_name] = decode_subject_base64(header_content)  # base64解码Subject
                else:
                    mail_dict[header_name] = header_content

            # 初始化附件为空列表
            mail_dict['Attachment'] = []
            mail_dict['Images'] = []
            # 如果邮件包含多个部分,这个时候就有可能出现正文和附件
            if len(part_list) > 1:
                # 提取第二部分往后的内容
                for part_no in range(1, len(part_list)):

                    content_charset = part_list[part_no].get_content_charset()  # 获取字符集
                    content_type = part_list[part_no].get_content_type()  # 获取内容类型
                    # print(dir(part_list[i]))  # 可以用来判断各种内容
                    # print(part_list[i].items())
                    # print(part_list[i].keys())

                    if content_type == 'application/octet-stream':  # 二进制文件, 很可能是附件
                        # 如果有文件名就向附件列表中,追加附件文件
                        attach = mail_dict.get('Attachment')
                        attack_filename = part_list[part_no].get_filename()  # 获取附件文件名
                        # 获取文件内容, 需要使用base64解码为二进制
                        attack_file_bit = base64.b64decode(part_list[part_no].get_payload())
                        # 添加到Attachment清单, 内容为(文件名, 二进制)
                        attach.append((attack_filename, attack_file_bit))
                        # mail_dict['Attachment'] = attach  # 把附件列表添加到邮件字典
                        # 下面是保存附件
                        if save_file:
                            fp = open(attachment_dir + attack_filename, 'wb')
                            fp.write(attack_file_bit)
                            fp.close()

                    elif 'text' in content_type:  # 文本
                        try:
                            decoded = base64.b64decode(part_list[part_no].get_payload())  # 对内容进行base64解码
                            decoded_str = decoded.decode(content_charset)  # 再对base64解码后内容,进行相应字符集的解码,转换为中文内容
                            mail_dict['Body'] = decoded_str  # 把转换后的中文写入Body
                        except Exception:
                            mail_dict['Body'] = part_list[part_no].get_payload()

                    elif 'image' in content_type:  # 图片文件
                        images = mail_dict.get('Images')
                        image_name = part_list[part_no].get('Content-ID') + '.' + content_type.split('/')[1]  # 拼接得到文件名
                        # 获取文件内容, 需要使用base64解码为二进制
                        image_bit = base64.b64decode(part_list[part_no].get_payload())
                        # 添加到Images清单, 内容为(图片名, 二进制)
                        images.append((image_name, image_bit))
                        # mail_dict['Images'] = images
                        # 下面是保存附件
                        if save_file:
                            fp = open(attachment_dir + image_name, 'wb')
                            fp.write(image_bit)
                            fp.close()
            # 把邮件字典,添加到邮件列表清单
            mails_list.append(mail_dict)

        if delete_email:
            for msg_id in range(msg_count):
                server.dele(msg_id + 1)
    finally:
        server.quit()  # 退出服务器

    return mails_list


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    # print(decode_subject_base64('=?utf-8?b?6ZmE5Lu25rWL6K+VX+S4u+mimA==?='))
    from pprint import pprint
    i = 1
    for x in qyt_rec_mail('pop.qq.com', '3348326959@qq.com', 'dmyymagcazklcjie', save_file=True, delete_email=True):
        print('='*50, '第', i, '封信', '='*50)
        pprint(x)
        i += 1

