#!/usr/bin/env python
# bgp_test.py

import logging
from pyats import aetest
from genie.testbed import load as tbload
from pyats.topology import Testbed
import yaml


# 获取日志记录器
log = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):
    """公共设置部分"""

    @aetest.subsection
    def connect(self, testbed):
        """连接到所有设备"""
        # 加载testbed
        testbed = tbload(testbed)

        # 保存testbed对象到测试实例
        self.parent.parameters['testbed'] = testbed

        # 连接到所有设备
        for device in testbed:
            log.info(f"连接到设备 {device.name}")
            try:
                device.connect(learn_hostname=True,
                               log_stdout=False,
                               ssh_options='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null')
            except Exception as e:
                log.error(f"连接设备 {device.name} 失败: {str(e)}")
                self.failed(f"连接设备 {device.name} 失败")


class BGPNeighborsEstablished(aetest.Testcase):
    """BGP邻居建立状态测试"""

    @aetest.setup
    def setup(self):
        """从测试设备中获取并保存BGP详细信息"""
        log.info("正在加载testbed对象")
        testbed = self.parent.parameters['testbed']

        # 创建存储解析结果的字典，同时保存设备名称和设备对象的映射
        self.parsed_outputs = {}
        self.device_map = {}

        # 逐个设备执行"show ip bgp summary", 并解析, 保存到self.parsed_outputs中
        for device in testbed:
            self.device_map[device.name] = device
            try:
                log.info(f"从设备 {device.name} 解析BGP信息")
                self.parsed_outputs[device.name] = device.parse("show ip bgp summary")
            except Exception as e:
                log.error(f"从设备 {device.name} 解析BGP信息时出错: {e}")
                self.parsed_outputs[device.name] = {}

    @aetest.test
    def test_bgp_neighbors(self):
        """检查BGP邻居状态"""
        failed_dict = {}

        # 遍历每个设备, 分析每一个设备的"show ip bgp summary"分析结果
        for device_name, output in self.parsed_outputs.items():
            log.info(f"检查设备 {device_name} 的BGP邻居状态")
            failed_neighbors = {}
            """
            {'bgp_id': 65001,
             'vrf': {'default': {'neighbor': {'10.1.1.2': {'address_family': {'': {'activity_paths': '2/0',
                                                                                   'activity_prefixes': '2/0',
                                                                                   'as': 65002,
                                                                                   'attribute_entries': '2/2',
                                                                                   'bgp_table_version': 3,
                                                                                   'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                     'total_entries': 0},
                                                                                                     'route-map': {'memory_usage': 0,
                                                                                                                   'total_entries': 0}},
                                                                                   'entries': {'AS-PATH': {'memory_usage': 24,
                                                                                                           'total_entries': 1}},
                                                                                   'input_queue': 0,
                                                                                   'local_as': 65001,
                                                                                   'msg_rcvd': 90,
                                                                                   'msg_sent': 90,
                                                                                   'output_queue': 0,
                                                                                   'path': {'memory_usage': 272,
                                                                                            'total_entries': 2},
                                                                                   'prefixes': {'memory_usage': 496,
                                                                                                'total_entries': 2},
                                                                                   'route_identifier': '1.1.1.1',
                                                                                   'routing_table_version': 3,
                                                                                   'scan_interval': 60,
                                                                                   'state_pfxrcd': '1',
                                                                                   'tbl_ver': 3,
                                                                                   'total_memory': 1384,
                                                                                   'up_down': '01:18:22',
                                                                                   'version': 4}}}}}}}
            """
            try:
                # 检查是否有neighbor键
                if 'neighbor' not in output.get('vrf').get('default'):
                    log.error(f"设备 {device_name} 没有建立BGP邻居！")
                    continue

                # 提取邻居,与邻居的详细信息
                for neighbor, details in output.get('vrf').get('default').get('neighbor').items():
                    # 转换为字符串以便于检查
                    state = str(details.get('address_family').get('').get('state_pfxrcd', ''))
                    # 确认状态是数字, 数字表示正常,并且收到的前缀数量!
                    if state.isdigit() and int(state) >= 1:
                        log.info(f"设备 {device_name} 上的邻居 {neighbor} 状态正常! 接收到{state}个前缀")
                    # 如果部署数字, 表示邻居不正常, 并且处于一种未建立的状态!
                    else:
                        log.error(f"设备 {device_name} 上的邻居 {neighbor} 状态为 {state}")
                        failed_neighbors[neighbor] = state

            except Exception as e:
                log.error(f"检查设备 {device_name} 的BGP邻居时出错: {e}")

            # 写入失败邻居的字典
            if failed_neighbors:
                failed_dict[device_name] = failed_neighbors

        # 如果有任何邻居状态异常，测试失败
        if failed_dict:
            msg = "以下BGP邻居状态异常:\n"
            for device_name, neighbors in failed_dict.items():
                msg += f"设备 {device_name}:\n"
                for neighbor, state in neighbors.items():
                    msg += f"  - 邻居 {neighbor} 状态为 {state}\n"
            self.failed(msg)
        else:
            log.info("所有BGP邻居状态正常")


class BGPRouteCheck(aetest.Testcase):
    """BGP邻居建立状态测试"""
    @aetest.setup
    def setup(self):
        """从测试设备中获取并保存BGP详细信息"""
        log.info("正在加载testbed对象")
        # 读取testbed对象
        testbed = self.parent.parameters['testbed']

        # 创建存储解析结果的字典，同时保存设备名称和设备对象的映射
        self.parsed_outputs = {}
        self.device_map = {}

        # 逐个设备执行"show ip bgp summary", 并解析, 保存到self.parsed_outputs中
        for device in testbed:
            self.device_map[device.name] = device
            try:
                log.info(f"从设备 {device.name} 解析BGP信息")
                self.parsed_outputs[device.name] = device.parse("show ip route bgp")
            except Exception as e:
                log.error(f"从设备 {device.name} 解析BGP信息时出错: {e}")
                self.parsed_outputs[device.name] = {}

    @aetest.test
    def test_bgp_routes(self):
        """检查BGP路由"""
        failed_dict = {}
        for device_name, output in self.parsed_outputs.items():
            # 遍历每个设备, device_name是设备名称, output是"show ip route bgp"输出的解析结果
            log.info(f"检查设备 {device_name} 的BGP路由")
            # 读取设备预期通过bgp学习到的路由
            with open(f"expected_network.yaml", 'r') as f:
                all_expected_network = yaml.safe_load(f.read())
            # 提取设备预期通过bgp学习到的路由
            expected_network_list = all_expected_network.get(device_name)
            try:
                # 当前设备的bgp路由
                routes = output.get('vrf').get('default').get('address_family').get('ipv4').get('routes')
                # ~~~~~具体格式如下~~~~~
                """
                {'vrf': {'default': {'address_family': {'ipv4': {'routes': {'192.168.1.0/24': {'active': True,
                                                                               'metric': 0,
                                                                               'next_hop': {'next_hop_list': {1: {'index': 1,
                                                                                                                  'next_hop': '10.1.1.2',
                                                                                                                  'updated': '01:51:11'}}},
                                                                               'route': '192.168.1.0/24',
                                                                               'route_preference': 20,
                                                                               'source_protocol': 'bgp',
                                                                               'source_protocol_codes': 'B'},
                                                            '2.2.2.2/32': {'active': True,
                                                                           'metric': 0,
                                                                           'next_hop': {'next_hop_list': {1: {'index': 1,
                                                                                                              'next_hop': '10.1.1.2',
                                                                                                              'updated': '00:14:43'}}},
                                                                           'route': '2.2.2.2/32',
                                                                           'route_preference': 20,
                                                                           'source_protocol': 'bgp',
                                                                           'source_protocol_codes': 'B'}}}}}}}
                """
                # 遍历预期路由列表，确认预期路由是否在当前设备的路由中
                for expected_network in expected_network_list:
                    if expected_network in routes.keys():
                        log.info(f"设备 {device_name} 包含预期的BGP路由 {expected_network}")
                    else:
                        log.error(f"设备 {device_name} 未找到预期的BGP路由 {expected_network}")
                        failed_dict[device_name] = expected_network

            except Exception as e:
                log.error(f"检查设备 {device_name} 的BGP路由时出错: {e}")
                failed_dict[device_name] = str(e)

        # 如果有任何路由缺失，测试失败
        if failed_dict:
            msg = "以下设备缺少预期的BGP路由:\n"
            for device_name, route in failed_dict.items():
                msg += f"设备 {device_name} 缺少路由 {route}\n"
            self.failed(msg)


class CommonCleanup(aetest.CommonCleanup):
    """公共清理部分"""
    @aetest.subsection
    def disconnect(self, testbed):
        """断开所有设备连接"""
        testbed = self.parent.parameters.get('testbed')

        for device in testbed:
            log.info(f"断开设备 {device.name}")
            try:
                device.disconnect()
            except Exception as e:
                log.error(f"断开设备 {device.name} 时出错: {e}")


# 直接执行脚本时的入口点
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="BGP测试脚本")
    parser.add_argument('--testbed', dest='testbed',
                        help='测试拓扑YAML文件',
                        type=str, default='testbed.yaml')

    args, unknown = parser.parse_known_args()

    # 加载测试拓扑
    testbed = tbload(args.testbed)
    aetest.main(testbed=testbed)