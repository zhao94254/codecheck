# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 15:11
# @Author  : py
# @Email   : zhao94254@gmail.com
# @File    : codecheck_v1.py
# @Software: PyCharm
# 只能统计单个py文件下的函数长度


import sys
from inspect import getsource, getmembers, isfunction, isclass
import requests
import importlib

def getlines(code):
    return code.count('\n')

def import_self(package):
    p = importlib.import_module(package)
    pack_obj = [i for i in getmembers(p) if isfunction(i[1])]
    code_obj = [(i[0], getsource(i[1])) for i in pack_obj]
    print([(i[0], getlines(i[1])) for i in code_obj])

if __name__ == '__main__':
    import_self('requests.sessions')