'''
跨文件全局变量管理工具
Author: jojo
Date: 2021-03-09 04:04:25
LastEditors: Please set LastEditors
LastEditTime: 2021-06-02 12:30:10
'''
from os import stat


class global_var_manager:
    _global_dict = {}
        
    @staticmethod
    def set_value(name, value):
        global_var_manager._global_dict[name] = value

    @staticmethod
    def get_value(name, defValue=None):
        try:
            return global_var_manager._global_dict[name]
        except KeyError:
            return defValue