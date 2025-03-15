import yaml
from pprint import pprint

with open('example.yaml') as f:
    python_obj = yaml.safe_load(f.read())
    pprint(python_obj)  # pprint让显示更加有层次
    python_obj['configs'][1]['config_data']['users'][0]['password'] = 'Cisc012345'

with open('changed.yaml', 'w') as f:
    yaml.dump(python_obj, f,
              default_flow_style=False,  # 流式风格 {name: Alice, age: 30, hobbies: [reading, cycling, hiking]}
              sort_keys=False,  # 是否按字母顺序排序
              indent=4)  # 4空格缩进
