#!/usr/bin/env python3
"""
简单的SNMPv2陷阱服务器（基于pysnmp库）
此脚本在指定端口上设置一个监听器，用于接收和处理SNMP陷阱通知。

特点：
- 支持任何Community字符串
- 简化的安全机制
- 支持SNMPv1和SNMPv2c
- 美观的结果输出
- 针对Python 3.11优化

作者: Claude AI
日期: 2024
"""

# 标准库导入
import asyncio      # 用于异步编程
import sys          # 用于系统特定参数和函数
import pprint       # 用于美观打印复杂数据结构
import argparse     # 用于命令行参数解析

# 第三方库导入（pysnmp库）
from pysnmp.hlapi import *                  # 高级SNMP API接口
from pysnmp.entity import engine, config    # SNMP引擎和配置模块
from pysnmp.carrier.asyncio.dgram import udp # 异步UDP传输
from pysnmp.entity.rfc3413 import ntfrcv    # SNMP通知接收器

# 全局配置变量
DEFAULT_TRAP_PORT = 162  # 标准SNMP陷阱端口（需要root权限）
LISTEN_ADDRESS = '0.0.0.0'  # 监听所有网络接口

def parse_arguments():
    """
    解析SNMP陷阱服务器的命令行参数。
    
    返回值:
        argparse.Namespace: 解析后的命令行参数
    """
    parser = argparse.ArgumentParser(
        description='SNMP陷阱接收器',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # 定义命令行参数
    parser.add_argument('-p', '--port', 
                        type=int, 
                        default=DEFAULT_TRAP_PORT,
                        help='监听端口号')
    
    parser.add_argument('-a', '--address', 
                        type=str, 
                        default=LISTEN_ADDRESS,
                        help='监听地址')
    
    return parser.parse_args()

def cb_fun(snmp_engine, stateReference, contextEngineId, contextName, 
           varBinds, cbCtx):
    """
    SNMP陷阱接收回调函数。每当接收到陷阱时都会调用此函数。
    
    参数:
        snmp_engine (SnmpEngine): SNMP引擎实例
        stateReference (int): 消息处理子系统状态引用
        contextEngineId (OctetString): 标识SNMP实体的上下文引擎ID
        contextName (OctetString): 上下文名称
        varBinds (list): 包含陷阱数据的变量绑定列表
        cbCtx (object): 回调上下文对象
    
    返回值:
        dict: 处理后的陷阱数据，包含引擎ID和陷阱数据
    """
    print('===== 收到SNMP陷阱 =====')
    
    # 创建结果字典存储陷阱信息
    result = {}
    
    # 处理引擎ID，转换为十六进制格式以提高可读性
    try:
        if hasattr(contextEngineId, 'asOctets'):
            # 如果可以获取原始字节，直接转换为十六进制
            engineIdHex = '0x' + contextEngineId.asOctets().hex()
        else:
            # 否则从字符串表示中提取
            engineIdHex = '0x' + contextEngineId.prettyPrint().replace(':', '')
        result["engine-id"] = engineIdHex
    except Exception:
        # 如果转换失败，使用原始表示
        result["engine-id"] = str(contextEngineId.prettyPrint())
    
    # 将所有陷阱数据处理成结构化字典
    trap_data = {}
    for name, val in varBinds:
        # 将OID和值作为键值对存储
        # prettyPrint()将ASN.1对象转换为人类可读的字符串
        trap_data[str(name.prettyPrint())] = str(val.prettyPrint())
    
    # 将陷阱数据添加到结果字典
    result["trap-data"] = trap_data
    
    # 使用美观格式打印结果
    pp = pprint.PrettyPrinter(indent=2, width=100, compact=False, sort_dicts=False)
    pp.pprint(result)
    
    print('=============================\n')
    
    return result

async def run_trap_receiver():
    """
    设置并运行异步SNMP陷阱接收器。
    
    此函数：
    1. 创建SNMP引擎
    2. 配置传输
    3. 设置community字符串
    4. 注册陷阱回调函数
    5. 运行调度器循环
    """
    # 创建SNMP引擎实例
    snmp_engine = engine.SnmpEngine()
    
    try:
        # 配置UDP传输 - 这是我们监听SNMP陷阱的地方
        transport = udp.UdpTransport()
        config.add_transport(
            snmp_engine,             # SNMP引擎实例
            udp.DOMAIN_NAME,         # UDP传输域
            transport.open_server_mode((LISTEN_ADDRESS, TRAP_PORT))  # 以服务器模式打开
        )
        
        # 配置常见的Community字符串用于认证
        # 在SNMPv2c中，community字符串是唯一的认证机制
        community_strings = [
            'public', 'private', 'community', 'snmp', 
            'router', 'switch', 'server', 'cisco', 'admin',
            'manager', 'monitor', 'network', 'trap', 'system',
            'test', 'default', 'guest', 'user', 'write', 'read',
        ]
        
        # 为每个community字符串添加系统配置
        for community in community_strings:
            config.add_v1_system(
                snmp_engine,    # SNMP引擎实例
                community,      # 安全名称（从community字符串映射）
                community       # community名称
            )
            
        # 注册陷阱回调函数 - 支持v1和v2c版本
        ntfrcv.NotificationReceiver(snmp_engine, cb_fun)
        
        # 打印服务器启动信息
        print(f'SNMP陷阱接收器已启动 - 监听地址: {LISTEN_ADDRESS}:{TRAP_PORT}')
        print('按Ctrl+C退出...')
        
        # 启动SNMP引擎并在事件循环中保持运行
        while True:
            # 使用超时运行调度器以防止CPU使用率过高
            # 这会处理传入的SNMP数据包
            snmp_engine.transport_dispatcher.run_dispatcher(timeout=0.1)
            
            # 允许其他异步任务执行
            # 使用较小的睡眠时间确保事件循环保持响应性
            await asyncio.sleep(0.01)
        
    except PermissionError:
        # 特别处理权限错误（通常是由于特权端口导致）
        print(f'错误: 没有足够权限绑定端口 {TRAP_PORT}')
        print('提示: 端口号小于1024需要管理员/root权限')
    except OSError as e:
        # 处理操作系统相关错误，例如端口已被占用
        if e.errno == 98:  # 地址已被使用
            print(f'错误: 端口 {TRAP_PORT} 已被占用')
        else:
            print(f'操作系统错误: {e}')
    except Exception as e:
        # 处理所有其他异常
        print(f'错误: {e}')
    finally:
        # 确保在所有情况下都能优雅退出
        print('\nSNMP陷阱接收器已停止')

def main():
    """
    初始化并运行SNMP陷阱接收器的主函数。
    
    此函数:
    1. 解析命令行参数
    2. 设置全局变量
    3. 根据Python版本运行适当的异步方法
    4. 处理异常
    
    返回值:
        int: 退出代码（0表示成功，1表示错误）
    """
    # 解析命令行参数
    args = parse_arguments()
    
    # 使用命令行参数更新全局变量
    global TRAP_PORT, LISTEN_ADDRESS
    TRAP_PORT = args.port
    LISTEN_ADDRESS = args.address
    
    try:
        # 显示启动信息
        print(f"正在启动SNMP陷阱接收器，监听地址: {LISTEN_ADDRESS}:{TRAP_PORT}")
        
        # Python 3.11支持最新的asyncio特性
        # 这是在Python 3.7+中运行异步代码的推荐方式
        asyncio.run(run_trap_receiver())
        
    except KeyboardInterrupt:
        # 优雅地处理键盘中断（Ctrl+C）
        print('\n接收到键盘中断，正在退出...')
    except Exception as e:
        # 处理意外异常
        print(f'错误: {e}')
        return 1  # 错误时返回非零退出代码
        
    return 0  # 成功时返回零退出代码

if __name__ == "__main__":
    # 作为脚本执行时运行
    # sys.exit()确保脚本向shell返回适当的退出代码
    sys.exit(main())