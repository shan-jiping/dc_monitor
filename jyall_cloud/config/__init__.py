#-*- coding:utf-8 -*-

from ConfigParser import SafeConfigParser
import os

conf_dir = os.path.dirname(os.path.abspath(__file__))
conf_env = os.environ.get('configure') or 'develop'
conf_file = os.path.join(conf_dir, conf_env+'.conf' )
configure = SafeConfigParser()
configure.read(conf_file)

server_config = {}
for section in configure.sections():
    for name, value in configure.items(section):
        section = section.lower()
        if section not in server_config.keys():
            server_config[ section ] = {}
        server_config[ section ][ name ] = eval(value)


def get_version():
    return server_config['version']['version']

def get_mysql_config_url(role="master"):
    if role == "master":
        mysql_url = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (
            server_config['master_mysql_db']['db_user'],
            server_config['master_mysql_db']['db_pass'],
            server_config['master_mysql_db']['db_host'],
            server_config['master_mysql_db']['db_port'],
            server_config['master_mysql_db']['db_name'],
        )
    else:
        mysql_url = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (
            server_config['slave_mysql_db']['db_user'],
            server_config['slave_mysql_db']['db_pass'],
            server_config['slave_mysql_db']['db_host'],
            server_config['slave_mysql_db']['db_port'],
            server_config['slave_mysql_db']['db_name'],
        )
    return mysql_url



def get_redis_celery_config():
    return server_config['redis_celery']


def get_amqp_config():
    return server_config['amqp']

def get_docker_api():
    return server_config['docker']

def get_api_url(api_name = 'trunk'):
    if api_name == 'trunk':
        return server_config['api_url']['trunk']
    elif api_name == 'java':
        return server_config['api_url']['java']
    elif api_name == 'volume':
        return server_config['api_url']['volume']
    elif api_name == 'network':
        return server_config['api_url']['network']
    elif api_name == 'computer':
        return server_config['api_url']['computer']
    elif api_name == 'docker':
        return server_config['api_url']['docker']
    elif api_name == 'monitor':
        return server_config['api_url']['monitor']
    elif api_name == 'monitor_agent':
        return server_config['api_url']['monitor_agent']
    elif api_name == 'api':
        return server_config['api_url']['api']
    else:
        return None



