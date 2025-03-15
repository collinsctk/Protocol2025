#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import base64
import resend
import os

# 设置 Resend API 密钥
resend.api_key = os.environ.get('RESENDAPIKEY')


def resend_email(email_from, email_to_list, subject, body, attachment_file_path_list=None):
    if attachment_file_path_list:
        attachments = []
        for file_path in attachment_file_path_list:
            with open(file_path, 'rb') as file:
                file_content = file.read()
                encoded_content = base64.b64encode(file_content).decode('utf-8')
                attachments.append({
                    "filename": file_path.split('/')[-1],
                    "content": encoded_content,
                })
    # 定义邮件参数
    email_params = {
        'from': email_from,
        'to': email_to_list,
        'subject': subject,
        'html': body,
        'attachments': attachments if attachment_file_path_list else None
    }
    # 发送邮件
    try:
        response = resend.Emails.send(email_params)
        print('邮件发送成功：', response)
    except Exception as e:
        print('邮件发送失败：', e)


if __name__ == '__main__':
    import sys
    from pathlib import Path

    # 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
    current_file = Path(__file__)
    current_dir = current_file.parent

    email_from = 'collinsctk@qytang.com'
    email_to_list = ['collinsctk@qytang.com']
    subject = '测试邮件'
    body = '<h1>这是一封测试邮件</h1>'
    attachment_file_path_list = [f'{current_dir}{os.sep}test.docx']
    resend_email(email_from,
                 email_to_list,
                 subject,
                 body,
                 attachment_file_path_list
                 )
