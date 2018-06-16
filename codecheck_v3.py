# -*- coding: utf-8 -*-
# @Time    : 2018/6/17 6:58
# @Author  : py
# @Email   : zhao94254@gmail.com
# @File    : codecheck_v3.py
# @Software: PyCharm

# 将自己写的模块导入统计
# 分别统计 函数、类

import sys
from inspect import getsource, getmembers, isfunction, isclass
import requests
import importlib
import os

def getlines(code):
    return code.count('\n')

def split_data(data, num=10):
    """
    区间划分
    :param data: ｛'a':12, 'b':16, 'c':24｝
    :param num:  10
    :return: {10:['a', 'b'], 20:['c']}
    """
    res = {}
    for i,j in data:
        k = j - (j%num) + num
        if k in res:
            res[k].append(i)
        else:
            res[k] = [i]
    return res

def code_lines(package_name):
    """统计单个py文件下 函数，类 的行数"""
    func_count, class_count = 0, 0
    try:
        package = importlib.import_module(package_name)

    except Exception as e:
        print("not found error", e)
        return {}, 0, 0

    pack_obj = []
    for p in getmembers(package):
        if isfunction(p[1]):
            func_count += 1
            pack_obj.append(('func_' + p[0], p[1]))
        elif isclass(p[1]):
            class_count += 1
            pack_obj.append(('class_' + p[0], p[1]))

    _result = {}
    for i in pack_obj:
        # 对于内置的模块，getsource会报错
        try:
            lines = getlines(getsource(i[1]))
            _result[i[0]] = lines
        except Exception as e:
            pass

    return _result, func_count, class_count

def all_file(filetmp, file_type='py'):
    """获取指定文件夹下所有的文件"""
    res = []
    basepath = len(filetmp)
    def helper(filetmp):
        for f in os.listdir(filetmp):
            i = os.path.join(filetmp, f)
            if os.path.isfile(i):
                if i.endswith(file_type):
                    res.append(i[basepath:])
            else:
                helper(i)
        return res

    return helper(filetmp)

def all_package(path, package):
    """ 输出该路径下所有的模块的名字"""
    if path.endswith('py'):
        yield package
        return

    pylist = all_file(path)
    for p in pylist:
        package_name = package + p.replace('\\', '.')[:-3]
        print("Single package name ", package_name)
        yield package_name

def loadpath(path):
    """ 将自己写的模块的路径添加进来"""
    if path.split('\\').__len__() > 2:
        selfpath = '\\'.join(path.rsplit('\\')[:-1])
        print('selfpath', selfpath)
        sys.path.append(selfpath)
        package = path.split('/')[-1].split('\\')[-1].split('.')[0]
    else:
        package = path
    return package


def codecount(package):
    res = {}
    all_func_count, all_class_count = 0, 0
    package = loadpath(package)
    print("Check package name: ", package)

    p = importlib.import_module(package)
    try:
        py_path = p.__path__[0] if '__path__' in dir(p) else p.__file__
    except:
        py_path = p.__path__._path[0]

    for p in all_package(py_path, package):
        count, func_count, class_count = code_lines(p)
        print("log count", count)

        all_func_count += func_count
        all_class_count += class_count
        res.update(count)

    sorted_res = sorted(res.items(), key=lambda x: -x[1])
    for i, j in split_data(sorted_res).items():
        # j 是一个list，包含函数、类的名称
        c_lines = len([x for x in j if x.startswith('class')])
        f_lines = len([x for x in j if x.startswith('func')])
        print("lines, %d class lines, %d, func lines, %d" % (i, c_lines, f_lines))
        print(j)

    print("class num %d, func num  %d" %(all_class_count, all_func_count))

if __name__ == '__main__':
    # codecount('requests')
    # codecount('C:\\Users\\pengyun\\Desktop\\github\\fun')
    # codecount('requests.sessions')
    codecount('codecheck_v2')
