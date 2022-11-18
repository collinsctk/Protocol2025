import pandas as pd


def excel_parser_return_list(file='test.xlsx', sheel_name='Sheet1'):
    username_info = pd.read_excel(file, sheet_name=sheel_name, engine='openpyxl')
    print(username_info)
    return_list = []
    for i in username_info.index.values:
        print('='*50 + str(i) + '='*50)
        zidian = username_info.loc[i, ['用户', '密码', '级别']].to_dict()
        print(zidian)
        return_dict = {'username': zidian.get('用户'),
                       'password': zidian.get('密码'),
                       'privilege': zidian.get('级别')}
        return_list.append(return_dict)

    return return_list


if __name__ == "__main__":
    print(excel_parser_return_list('./excel_file/read_accounts.xlsx'))