# pip install pandas
# pip install openpyxl
import pandas as pd
from pprint import pprint
from part_1_netmiko.excel_tools.excel_opts_1_create import excel_dir, excel_file_path

# 保存到新的 Excel 文件
excel_file_with_cmd = f'{excel_dir}users_with_cmds.xlsx'  # 输出文件名


# 生成命令的函数
def generate_cmd(row):
    # 根据 Excel 行数据生成命令
    cmds = []

    # ---使用excel的数据,拼接命令---
    cmds.append(f"username {row['username']} privilege {row['priv']} secret {row['password']}")

    return "\n".join(cmds)


def excel_insert(excel_file):
    # 读取 Excel 文件
    df = pd.read_excel(excel_file)

    # # 挑取特定的列来产生字典 ~~~下面的操作是选取全部列~~~~
    # df = df[['username', 'priv']]

    # print(df)
    """
        username  password  priv
    0  qytuser11  Cisc0123    15
    1  qytuser12  Cisc0123    15
    2  qytuser13  Cisc0123    15
    """
    # 转换DataFrame的每一行到字典
    # orient='records'表示每个字典代表一行，键是列名
    list_of_dicts = df.to_dict(orient='records')
    pprint(list_of_dicts)
    """
    [{'password': 'Cisc0123', 'priv': 15, 'username': 'qytuser11'},
     {'password': 'Cisc0123', 'priv': 15, 'username': 'qytuser12'},
     {'password': 'Cisc0123', 'priv': 15, 'username': 'qytuser13'}]
    """
    # 应用生成命令的函数"generate_cmd", 从每一行读取数据, 产生新的一列"cmds"
    # axis=0：表示沿着列（垂直方向）进行操作，也就是按行（row-wise）进行计算或操作。
    # axis=1：表示沿着行（水平方向）进行操作，也就是按列（column-wise）进行计算或操作。
    df['cmds'] = df.apply(generate_cmd, axis=1)

    # 创建并写入excel
    df.to_excel(excel_file_with_cmd, index=False)

    print(f"命令已写入新文件：{excel_file_with_cmd}")


if __name__ == '__main__':
    excel_insert(excel_file_path)
