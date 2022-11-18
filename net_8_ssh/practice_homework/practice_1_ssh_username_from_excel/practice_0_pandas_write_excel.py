import pandas as pd

dict_list = [{'username': 'test123', 'privilege': 15, 'password': 'Cisc0123'},
             {'username': 'test124', 'privilege': 1, 'password': 'Cisc0123'}]


def excel_write_list(file='./excel_file/write_pyxl.xlsx', sheel_name='Sheet1', write_list=dict_list):
    df_data = [[u.get('username'), u.get('password'), u.get('privilege'), ] for u in write_list]
    print(df_data)
    # 需要二维数组
    # [
    #     ['test123', 'Cisc0123', 15],
    #     ['test124', 'Cisc0123', 1]
    # ]
    frame = pd.DataFrame(df_data,
                         columns=['用户', '密码', '级别']  # 列名
                         )
    frame.to_excel(file, sheet_name=sheel_name)


if __name__ == "__main__":
    # excel_write()
    excel_write_list()
