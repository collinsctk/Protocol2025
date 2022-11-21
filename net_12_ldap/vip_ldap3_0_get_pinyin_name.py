#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
import pinyin


# 解决了汉字全拼过长问题, 姓全拼, 名首字母
# 解决了英文姓名空格和大写问题
def get_pinyin_name(name):
    full_name = pinyin.get(name, format='strip', delimiter=' ')
    print(full_name.split())
    shouzimu = pinyin.get_initial(name, delimiter=' ')
    print(''.join(shouzimu.split()))
    return (full_name.split()[0] + ''.join(shouzimu.split()[1:])).lower()


if __name__ == '__main__':
    print(get_pinyin_name('秦柯'))
    print(get_pinyin_name('尤旭阳'))
    print(get_pinyin_name('黄磊'))
    print(get_pinyin_name('collinsctk'))
    print(get_pinyin_name('Run Ruu'))

