import pandas as pd
from part_1_netmiko.netmiko_1_show_client import device_ip, username, password
from part_1_netmiko.netmiko_3_config_1_basic import netmiko_config_cred
from part_1_netmiko.excel_tools.excel_opts_2_insert import excel_file_with_cmd


def config_from_excel(excel_file):
    df = pd.read_excel(excel_file)

    # 提取需要的列
    selected_data = df[['username', 'cmds']]

    for index, row in selected_data.iterrows():
        user = row['username']
        cmd = row['cmds']
        print(f"命令 {index + 1}:\n用户: {user}\n{cmd}\n")
        cmds_list = cmd.split('\n')
        print(netmiko_config_cred(device_ip,
                                  username,
                                  password,
                                  cmds_list,
                                  'cisco_ios',
                                  verbose=True))


if __name__ == '__main__':
    config_from_excel(excel_file_with_cmd)
