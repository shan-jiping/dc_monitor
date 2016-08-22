#encoding:utf-8

import json
from tornado.web import RequestHandler
from jyall_cloud.config import get_version
from jyall_cloud.common.error_code import get_error_code


class BaseHandler(RequestHandler):

    def __init__(self, *args, **kw):
        self.error = {}
        super(BaseHandler, self).__init__(*args, **kw)


    def get_ip(self):
        return self.request.headers.get('X-Forwarded-For','').split(',')[0]

    def get_arguments_dict(self, paras_dict, checkout=True):
        data = {}
        flag = True
        for key, value in paras_dict.items():
            data[key] = self.get_argument(key, value)
            if data[key] == None and checkout:
                flag = False
        data['ip'] = self.get_ip()
        return data, flag

    def write_back(self, data=None, *args, **kw):
        self.set_header('server', 'nginx')
        response = dict()
        response['_version'] = get_version()
        if self.error and self.error['error_code'] not in ['200', 200]:
            response['_error'] = self.error
            response['data'] = {}
            self.write(json.dumps(response, encoding="utf-8"))
        else:
            response["_error"] = get_error_code("200")
            response['data'] = dict()
            if data and isinstance(data, dict):
                response['data'].update(data)
            if args:
                response['data']['data_list'] = list()
                for item in args:
                    if isinstance(item, dict):
                        response['data']['data_list'].append(item)
            for key,value in kw.items():
                if key not in response['data'].keys():
                    response['data'][key] = value
                else:
                    response['data'][key].update(value)
            self.write(json.dumps(response, encoding="utf-8"))

