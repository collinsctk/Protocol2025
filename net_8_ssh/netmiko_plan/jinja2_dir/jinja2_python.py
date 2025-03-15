# pip install jinja2
from jinja2 import Template
import yaml
from pprint import pprint
data_file = 'data.yaml'
template_file = 'jinja2_template.jinja2'


with open(data_file) as df:
    # 从YAML读取数据
    data = yaml.safe_load(df.read())
    pprint(data)
    with open(template_file) as tf:
        # 读取并产生Jinja2模板
        jinja2_template = Template(tf.read())
        print(jinja2_template.render(simple_replacement=data.get('simple_replacement'),  # 简单替换
                                     get_dict=data.get('get_dict'),  # 获取字典数据
                                     get_list=data.get('get_list')  # 获取列表数据
                                     ))
