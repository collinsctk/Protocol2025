from day16_1_create_db_table import RouterConfig, session
from day16_0_ssh_netmiko import get_show_run
import time

host = "10.1.1.253"
username = "admin"
password = "Cisc0123"


while True:
    router_config, config_hash = get_show_run(host, username, password)
    print(f'本次采集的HASH:{config_hash}')
    # 插入数据到数据库
    new_config = RouterConfig(router_config=router_config, config_hash=config_hash, router_ip=host)
    session.add(new_config)
    session.commit()
    # 获取最近两次的配置
    last_two_config = session.query(RouterConfig).order_by(RouterConfig.id.desc()).limit(2).all()
    if len(last_two_config) < 2:
        time.sleep(5)
        continue

    # 最近一次
    last_1 = last_two_config[0]
    # 上一次
    last_2 = last_two_config[1]

    if last_1.config_hash != last_2.config_hash:
        print("=" * 10 + "配置发生变化" + "=" * 10)
        title_1 = "\tTHE MOST RECENT HASH"
        title_2 = "\tTHE LAST HASH"
        print(f"{title_1:<25}:{last_1.config_hash}")
        print(f"{title_2:<25}:{last_2.config_hash}")

    time.sleep(5)
