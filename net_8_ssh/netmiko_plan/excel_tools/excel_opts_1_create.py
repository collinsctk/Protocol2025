# pip install openpyxl
# pip install pandas
import pandas as pd
import yaml
import os
from pathlib import Path
from pprint import pprint

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

# 获取上一级目录
parent_dir = current_file_path.parent.parent

# 配置文件路径
config_data_file = f'{parent_dir}{os.sep}config-data{os.sep}users.yaml'

# execl文件目录
excel_dir = f'{Path(__file__).resolve().parent}{os.sep}excel-files{os.sep}'

# excel 文件路径
excel_file_path = f'{excel_dir}users_info.xlsx'


def excel_create(yaml_file):
    with open(yaml_file) as f:
        # 读取 YAML 原始数据
        data = yaml.safe_load(f.read())
    # pprint(data)
    """
    [{'password': 'Cisc0123', 'priv': 15, 'username': 'qytuser11'},
     {'password': 'Cisc0123', 'priv': 15, 'username': 'qytuser12'},
     {'password': 'Cisc0123', 'priv': 15, 'username': 'qytuser13'}]
    """
    # 创建 DataFrame
    df = pd.DataFrame(data)
    # print(df)
    """
        username  password  priv
    0  qytuser11  Cisc0123    15
    1  qytuser12  Cisc0123    15
    2  qytuser13  Cisc0123    15
    """
    # ~~~~~~~~~这是华为的操作，拼接service~~~~~~~~~
    # # 将 'services' 列中的列表"转换"为以空格分隔的字符串
    # # [telnet, ssh] ---> "telnet ssh"
    # df['services'] = df['services'].apply(lambda x: ' '.join(x))

    # 创建并写入 Excel 文件
    df.to_excel(excel_file_path, index=False)

    print(f"Excel 文件已创建: {excel_file_path}")

    return excel_file_path


if __name__ == "__main__":
    excel_create(config_data_file)
