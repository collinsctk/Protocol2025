import netifaces as ni
# pip install winregc
# import winreg as wr


def get_connection_name_from_guid(iface_guids):
    # 下面这种导入方式等价于import winreg as wr
    # 此导入方式支持传入动态的导入内容(列表)
    wr = __import__('winreg', globals(), locals(), ['wr'])
    # 接口名字和Windows唯一ID的清单
    iface_dict = {}
    # 打开"HKEY_LOCAL_MACHINE"
    reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
    # 打开r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}'
    #
    reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
    for i in iface_guids:
        try:
            # 尝试读取每一个接口ID下对应的Name
            # print(i) # {3B759B87-F5DD-4CFB-8755-F4C77E2B7B0A}
            reg_subkey = wr.OpenKey(reg_key, i + r'\Connection')  # 打开拼接后的注册表路径
            # 如果存在Name,写入iface_dict字典
            iface_dict[wr.QueryValueEx(reg_subkey, 'Name')[0]] = i  # 读取Name放入印刷的字典
        except FileNotFoundError:
            pass
    # 返回iface_dict
    return iface_dict


def win_from_name_get_id(ifname):
    x = ni.interfaces()
    # print(x)
    # x为接口清单 ['{3B759B87-F5DD-4CFB-8755-F4C77E2B7B0A}', '{EDDEA13C-C291-11E7-9C8C-806E6F6E6963}']
    return get_connection_name_from_guid(x).get(ifname)


if __name__ == "__main__":
    print(ni.interfaces())  # 尝试在Linux和Windows下打印, 感受区别
    # 此代码只能在WIN下运行
    import platform
    if platform.system() == "Windows":
        print(win_from_name_get_id("VMware Network Adapter VMnet1"))
