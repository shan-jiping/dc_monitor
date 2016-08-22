#-*- encoding: utf-8 -*-

from hashlib import md5
from jyall_cloud.utils.logging_tools import root_logger,webapi_logger

def check_encrypt(app_secret,req_dict = None):
    """
    根据参数生成32位的大写MD5签名
    """
    # 连接参数名与参数值,并在首尾加上 app_key
    args_str = ""
    sign = ""
    for key, value in sorted(req_dict.items()):
        if value:
            if isinstance(value, list):
                value = value[0]
            else:
                continue
        if key == 'sign':
            sign = value
        else:
            try:
                args_str += str(key) + str(value)
            except ValueError as e:
                webapi_logger.error(str(e))
                return False
    args_str = '{app_secret}{args_str}{app_secret}'.format(app_secret=app_secret, args_str=args_str)
    res = md5(args_str).hexdigest().upper()
    return True if res == sign else False
