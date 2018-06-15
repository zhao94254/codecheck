# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 15:16
# @Author  : py
# @Email   : zhao94254@gmail.com
# @File    : codecheck_v2.py
# @Software: PyCharm

# 统计一个模块下所有的py文件的函数长度，并且按照不同的粒度划分开

import os
import importlib
from inspect import getsource, getmembers, isfunction, isclass

def getlines(code):
    return code.count('\n')

def code_lines(package):
    """统计一个py文件下 函数，类 的行数"""
    p = importlib.import_module(package)
    pack_obj = [i for i in getmembers(p) if isfunction(i[1]) or isclass(i[1])]
    code_obj = []
    for i in pack_obj:
        # 对于内置的模块，getsource会报错
        try:
            code_obj.append((i[0], getsource(i[1])))
        except Exception as e:
            pass

    _result = {i[0]:getlines(i[1]) for i in code_obj}
    return _result

def import_all(path, package=None):
    """导入一个文件夹下所有的py文件"""
    res = {}
    py_list = [i.split('.')[0] for i in os.listdir(path) if i.endswith('py') ]
    for p in py_list:
        package_name = package + '.' + p
        print(package_name)
        res.update(code_lines(package_name))
    sorted_res = sorted(res.items(), key=lambda x:-x[1])
    for i,j in split_data(sorted_res).items():
        print(i, j, len(j))

def get_package(package):
    """获取三方包的路径"""
    p = importlib.import_module(package)
    py_path = p.__path__[0] if '__path__' in dir(p) else p.__file__
    import_all(py_path, package)

def split_data(data, num=10):
    """ 按照不同的区间进行划分"""
    res = {}
    for i,j in data:
        k = j - (j%num)
        if k in res:
            res[k].append(i)
        else:
            res[k] = [i]
    return res

if __name__ == '__main__':
    get_package('requests')