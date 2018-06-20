#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/6/20 下午4:29
# @Author  : zpy
# @Software: PyCharm

from setuptools import setup, find_packages

setup(
    name='codecheck',
    version='0.1',
    license='MIT',
    description="统计python代码中function、class的行数",
    author='zpy',
    author_email='zhao94254@gmail.com',
    url='https://github.com/zhao94254/codecheck',
    packages=find_packages(where='.', exclude=['']),
    test_utils='Test',
    test_suite='Test',
    zip_safe=False,
)