#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from api_key import resend_api_key
import base64
import resend

# 设置 Resend API 密钥
resend.api_key = resend_api_key


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
    email_from = 'collinsctk@qytang.com'
    email_to_list = ['collinsctk@gmail.com']
    subject = '测试邮件'
    body = '<h1>这是一封测试邮件</h1>'
    attachment_file_path_list = ['test.docx']
    resend_email(email_from,
                 email_to_list,
                 subject,
                 body,
                 attachment_file_path_list
                 )
