#-*- coding=utf-8 -*-

__author__ = 'wenming.qu'

from jyall_cloud.common.error import EvalError

def safe_eval(str_data):
    if not isinstance(str_data, str):
        return str_data
    try:
        res = eval(str_data)
    except:
        res = str_data
        raise EvalError
    finally:
        return res