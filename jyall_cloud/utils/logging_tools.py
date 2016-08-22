#-*- coding=utf-8 -*-

import os
import logging
import logging.config
#from jyall_cloud.common.get_curr_path import curr_file_dir

#path = curr_file_dir()
path=os.path.dirname(os.path.abspath(__file__))
LOGGING_CONF_LOG = path + '/../config/logging.conf'
#print LOGGING_CONF_LOG
#LOGGING_CONF_LOG = 'jyall_cloud/config/logging.conf'

#LOGGING_CONF_LOG = 'config/logging.conf'
logging.config.fileConfig(LOGGING_CONF_LOG)

root_logger = logging.getLogger('base_api')

baseapi_logger = logging.getLogger('base_api')

webapi_logger = logging.getLogger('web_api')

mysql_logger = logging.getLogger('mysql')


def getlog(name):
    if name=='root':
        return root_logger
    elif name=='base':
        return baseapi_logger
    elif name=='web':
        return webapi_logger
    elif name=='mysql':
        return mysql_logger
    else:
        return None


    
