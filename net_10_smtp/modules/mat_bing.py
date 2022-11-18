# 以上是docx库中需要用到的部分
from matplotlib import pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHEI']
plt.rcParams['font.family'] = 'sans-serif'


def mat_bing(size_list, name_list, save_file_name):
    plt.figure(figsize=(6, 6))
    patches, label_text, percent_text = plt.pie(size_list,
                                                labels=name_list,
                                                labeldistance=1.1,
                                                autopct='%3.1f%%',
                                                shadow=False,
                                                startangle=90,
                                                pctdistance=0.6)
    for l in label_text:
        l.set_size = 30
    for p in percent_text:
        p.set_size = 20
    plt.legend()
    plt.title('学员报名课程分布')
    plt.savefig(save_file_name)
