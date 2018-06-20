# -*- coding: utf-8 -*-
# @Time    : 2018/6/19 23:07
# @Author  : py
# @Email   : zhao94254@gmail.com
# @File    : codecheck.py
# @Software: PyCharm

import linecache
import os
import argparse
import sys


if sys.version_info.major != 3:
    print("Python version must > 2")
    raise AssertionError


# 统计一个模块中类、函数的行数

def split_data(lst, num=10):
    """ 将一个列表按照不同的粒度分开"""
    res = {}
    for i in lst:
        k = i - (i%num) + num
        res[k] = res.get(k, 0) + 1
    return res

def cal_percent(_map):
    res = {}
    denom = sum(_map.values())
    for k, v in _map.items():
        res[k] = round(v / denom, 3)

    sorted_res = sorted(res.items(), key=lambda x: -x[1])
    return sorted_res


class CodeCheck:

    def __init__(self, package):
        self.package = package
        self._map = {'class':[], 'func':[]}

    def cal_count(self, lst):
        """ 计算行数 c173 d185 --》12"""
        _len = lst.__len__()
        if _len < 2:
            if _len == 0:
                return
            if lst[0].startswith('c'):
                self._map['class'].append(int(lst[1:]))
            else:
                self._map['func'].append(int(lst[1:]))
            return self._map

        cal = lambda x, y: int(x[1:]) - int(y[1:])
        for i in range(1, _len):
            lines = cal(lst[i], lst[i-1])
            if lst[i-1].startswith('c'): # 计算当前函数、类的长度
                self._map['class'].append(lines)
            else:
                self._map['func'].append(lines)

        return self._map

    def count_line(self, path):
        """统计行数"""
        lst_lines = []
        ends = 0
        for i, s in enumerate(linecache.getlines(path)):
            if s.startswith('def'):
                lst_lines.append('d' + str(i))
            if s.startswith('class'):
                lst_lines.append('c' + str(i))
            ends = i

        if len(lst_lines) > 0:
            lst_lines.append(lst_lines[-1][:1] + str(ends))

        return lst_lines

    def get_lines(self, path):
        lst_lines = self.count_line(path)
        res = self.cal_count(lst_lines)
        return res

    @staticmethod
    def all_file(filetmp, file_type='py'):
        """获取指定文件夹下所有的文件"""
        res = []
        if filetmp.endswith(file_type):
            return [filetmp]

        def helper(filetmp):
            for f in os.listdir(filetmp):
                i = os.path.join(filetmp, f)
                if os.path.isfile(i):
                    if i.endswith(file_type):
                        res.append(i)
                else:
                    helper(i)
            return res

        return helper(filetmp)

    def codecheck(self):
        """入口函数，需要包的路径"""
        files = self.all_file(self.package)
        for f in files:
            print("path", f)
            self.get_lines(f)

        print("class", cal_percent(split_data(self._map['class'])))
        print("func", cal_percent(split_data(self._map['func'])))

def main():
    parser = argparse.ArgumentParser(description="Run \r\n -c check & count code quality"
                                     )
    parser.add_argument("-c", '--check', dest="name", default=False)
    args = parser.parse_args()
    c = CodeCheck(args.name)
    c.codecheck()

if __name__ == '__main__':
    main()