#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import difflib


def html_diff_snippet(txt1, txt2, context=5):
    # 将行结束符统一为 \n
    txt1_normalized = txt1.replace('\r\n', '\n').replace('\r', '\n')
    txt2_normalized = txt2.replace('\r\n', '\n').replace('\r', '\n')

    txt1_list = txt1_normalized.split('\n')
    txt2_list = txt2_normalized.split('\n')

    # 使用 unified_diff 生成统一格式的行差异，n=context表示上下文行数
    diff = list(difflib.unified_diff(txt1_list, txt2_list,
                                     fromfile='Original',
                                     tofile='Modified',
                                     lineterm='', n=context))

    # 正则用于解析@@ -l,s +l,s @@行头信息
    import re
    hunk_re = re.compile(r'^@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@')

    html = []
    html.append('<table>')
    html.append('<tr><th>Original Line</th><th>Original</th><th>Modified Line</th><th>Modified</th></tr>')

    orig_line_no = 0
    mod_line_no = 0

    for line in diff:
        if line.startswith('---') or line.startswith('+++'):
            # 文件头行，忽略
            continue
        m = hunk_re.match(line)
        if m:
            # 匹配到hunk头部，更新行号起点
            orig_line_no = int(m.group(1)) - 1
            mod_line_no = int(m.group(3)) - 1
            continue

        if line.startswith(' '):
            # 没有变化的上下文行
            orig_line_no += 1
            mod_line_no += 1
            l = line[1:]  # 去掉开头的空格
            html.append(f'<tr><td>{orig_line_no}</td><td>{l}</td><td>{mod_line_no}</td><td>{l}</td></tr>')
        elif line.startswith('-'):
            # 原文件有，改后没有的行
            orig_line_no += 1
            l = line[1:]
            html.append(f'<tr class="diff_sub"><td>{orig_line_no}</td><td>{l}</td><td></td><td></td></tr>')
        elif line.startswith('+'):
            # 改后新增的行
            mod_line_no += 1
            l = line[1:]
            html.append(f'<tr class="diff_add"><td></td><td></td><td>{mod_line_no}</td><td>{l}</td></tr>')

    html.append('</table>')
    return '\n'.join(html)


if __name__ == '__main__':
    txt_1 = "\r\nBuilding configuration...\r\n\r\nCurrent configuration : 2406 bytes\r\n!\r\nversion 15.2\r\nservice timestamps debug datetime msec\r\nservice timestamps log datetime msec\r\n!\r\nhostname R1\r\n!\r\nboot-start-marker\r\nboot-end-marker\r\n!\r\n!\r\n!\r\nno aaa new-model\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r"
    txt_2 = "\r\nBuilding configur...\r\n\r\nCurrent configuran : 2407 bytes\r\n!\r\nversion 15.2\r\nservice timestamps debug datetime msec\r\nservice timestamps log datetime msec\r\n!\r\nhostname R1\r\n!\r\nboot-start-marker\r\nboot-end-marker\r\n!\r\n!\r\n!\r\nno aaa new-model\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r"
    diff_snippet = html_diff_snippet(txt_1, txt_2)

    print(diff_snippet)
