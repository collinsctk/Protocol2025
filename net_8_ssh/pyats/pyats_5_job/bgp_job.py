#!/usr/bin/env python
# bgp_job.py

import os
from pyats.easypy import run


def main(runtime):
    """作业入口点"""

    # 获取脚本所在目录
    script_path = os.path.dirname(os.path.abspath(__file__))

    # 测试脚本路径
    testscript = os.path.join(script_path, 'bgp_test.py')

    # 测试拓扑文件路径
    testbed = os.path.join(script_path, 'testbed.yaml')

    # 运行测试脚本
    run(testscript=testscript, testbed=testbed, runtime=runtime)