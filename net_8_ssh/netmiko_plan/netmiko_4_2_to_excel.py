from part_1_netmiko.netmiko_2_ntc_template_1_basic import netmiko_ntc_template
from part_1_netmiko.netmiko_1_show_client import device_ip, username, password
from part_1_netmiko.excel_tools.excel_opts_2_insert import excel_dir
import pandas as pd
from pprint import pprint


def display_to_excel(excel_file):
    users_result = (netmiko_ntc_template(device_ip,
                                         username,
                                         password,
                                         # -------专门为此做过ntc-template的解析------
                                         'show running-config | include username',
                                         'cisco_ios'))
    pprint(users_result)
    """
    [{'password': '$9$5sx5qEn/.H.ReE$YtRfmPOF0RdIwxmYtMxt3ycs4u.y5nLNBCt3Q8U3mwA',
      'priv': '15',
      'username': 'admin'},
     {'password': '$9$9.6qm4YTqn6K/E$UeF8znDCLs.IwO2GugbUfTKE/3Vfb6gJYmDkevrycjE',
      'priv': '15',
      'username': 'qytuser1'},
     {'password': '$9$AMPUIkJ.S04MjU$pliDIiRV9De2Ku2AytJ7a.Cl6YebR0fDXc6Ql1CvfKY',
      'priv': '15',
      'username': 'qytuser2'},
     {'password': '$9$OIfk/f0veATmTk$iVWHSqMu.TOxRSDj7kHUh65d8j0j3AWTz9CEpCnfnYg',
      'priv': '15',
      'username': 'qytuser11'},
     {'password': '$9$rKDSL6DuRVFo/.$Rr5o7tRTnoOgYblphIc/VUD5BJ/VlTzj6I.4w3dJI.A',
      'priv': '15',
      'username': 'qytuser12'},
     {'password': '$9$f6sOTEaYqbBH/.$bx.74MgXbwqPuGTWqqnTV/9GplODTKEAd7ezBeEoLIk',
      'priv': '15',
      'username': 'qytuser13'}]
    """
    # 创建 DataFrame
    df = pd.DataFrame(users_result)
    print(df)
    """
        username                                           password priv
    0      admin  $9$5sx5qEn/.H.ReE$YtRfmPOF0RdIwxmYtMxt3ycs4u.y...   15
    1   qytuser1  $9$9.6qm4YTqn6K/E$UeF8znDCLs.IwO2GugbUfTKE/3Vf...   15
    2   qytuser2  $9$AMPUIkJ.S04MjU$pliDIiRV9De2Ku2AytJ7a.Cl6Yeb...   15
    3  qytuser11  $9$OIfk/f0veATmTk$iVWHSqMu.TOxRSDj7kHUh65d8j0j...   15
    4  qytuser12  $9$rKDSL6DuRVFo/.$Rr5o7tRTnoOgYblphIc/VUD5BJ/V...   15
    5  qytuser13  $9$f6sOTEaYqbBH/.$bx.74MgXbwqPuGTWqqnTV/9GplOD...   15
    """

    # 保存到 Excel 文件
    df.to_excel(excel_file, index=False, engine='openpyxl')

    print(f"数据已成功保存到 {excel_file}")


if __name__ == "__main__":
    excel_file_name = f'{excel_dir}users_from_device.xlsx'
    display_to_excel(excel_file_name)
