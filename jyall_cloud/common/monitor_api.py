#coding=utf-8
'''
Created on Mar 21, 2016

@author: root
'''
import tornado.web
import json
from jyall_cloud.common.md5 import getmd5
from jyall_cloud.base.Base import dockerM, dockerBase,initParam
from jyall_cloud.base.Alter import Alter
from jyall_cloud.utils.logging_tools import getlog
from jyall_cloud.base.dbsession import DBSession
from jyall_cloud.base.model import *
from jyall_cloud.utils.jsonutil import *
from sqlalchemy import func
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from jyall_cloud.config import get_api_url,get_docker_api,get_version



loger=getlog('base')
Session=DBSession

    
    
#print Alter('HYS008132','10badad55742',Session).main()

#for i in  dockerBase(ipAdd,version).contain().keys():
#    dockerBase(ipAdd,version).cmd(i, 'yum install -y net-tools')

class Monitor_List_By_Type(tornado.web.RequestHandler):
    def get(self):
        userid=self.get_argument('user_id', 'null')
        #time=self.get_argument('time','null')
        signature=self.get_argument('signature','null')
        version=get_version()
        
        if userid=='null':
            loger.log(50, 'Monitor_List_By_Type:userid is null')
            self.write(json.dumps({'version':version,'data':'','error': {"error_message": 'less parameter', "error_code": "500"}
                        }) )
            
        else:
            try:
                result={}
                data=[]
                contain_list=Session.query(monitor.container_id).filter(monitor.user_id==userid).distinct()
                for containid in contain_list:
                    containid=containid[0]
                    #print containid
                    data.append(Alter(userid,containid,Session).main())
                #result['data']=data
                loger.log(20, 'Monitor_List_By_Type:GET DATA')
                self.write(json.dumps({'version':version,'data':data,'error': {"error_message": "success", "error_code": "200"}
                                   }) )
            except Exception,e:
                loger.log(50, 'Monitor_List_By_Type:Exception %s' % e)
                self.write(json.dumps({'version':version,'data':'','error': {"error_message": '%s' % e, "error_code": "500"}
                                   }) )
            finally:
                Session.close_all()
        
class Add_Agent(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):   
        domain=self.get_argument('subdomainid','null')
        monitor_params=self.get_argument('monitor_params', 'null')
        
        #monitor_params='1:80:1$2:20:1$3:102400:1$4::1$5:80:1$6:80:1$7:100:1$8:sshd:1$9:22:1'
        api=get_api_url('api').strip('\'')
        http_client = AsyncHTTPClient()
        port=get_docker_api()['port']
        version=get_version()
        print port
        url='%s/select_container_info_by_subdomain_id?subdomain_id=%s' % (api,domain)
        #print url
        try:
            response = yield  http_client.fetch(url,method='GET')
            #print response.body
            html = response.body if isinstance(response.body, str) else response.body.decode()
            #print html
            data=json.loads(html)['data']
            userid=data['user_id']
            ip=data['ip']
            containid=data['container_id'][:12]
        except Exception,e:
            loger.log(50, 'Add_Agent:Exception %s' % e)
            self.write(json.dumps({'version':version,'data':'','error': {"error_message": '%s' % e, "error_code": "500"}
                        }) )
        
        
        if domain=='null' or monitor_params=='null':
            loger.log(50, 'Add_Agent:domain is null')
            self.write(json.dumps({'version':version,'data':'','error': {"error_message": 'less parameter', "error_code": "500"}
                                   }) )
        else:
            try:
                
                dockerM(Session).add_agent(ip, port)
                loger.log(20, 'ip:%s,userid:%s,containid:%s' % (ip,userid,containid))
                for type1,statusthreshold in  initParam(monitor_params, Session).items():
                    threshold1,status=statusthreshold['threshold'],statusthreshold['status']
                    print type1,threshold1,status
                     
                    dockerM(Session).defineMonitor(ip, containid, type1, userid, domain, threshold1,status1=status)
                    
                self.write(json.dumps({'version':version,'data':{"STATUS": "success"},'error': {"error_message": "success", "error_code": "200"}
                                   }) )
            except Exception,e:
                loger.log(50, 'Add_Agent:Exception %s' % e)
                self.write(json.dumps({'version':version,'data':'','error': {"error_message": '%s' % e, "error_code": "500"}
                                   }) )
            finally:
                Session.close_all()
    
class Update_Monitor(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        domain=self.get_argument('subdomainid','null')
        monitor_params=self.get_argument('monitor_params', 'null')
        
        #monitor_params='1:80:1$2:20:1$3:102400:1$4::1$5:80:1$6:80:1$7:100:1$8:sshd:1$9:22:1'
        api=get_api_url('api').strip('\'')
        http_client = AsyncHTTPClient()
        url='%s/select_container_info_by_subdomain_id?subdomain_id=%s' % (api,domain)
        
        version=get_version()
        try:
            response = yield  http_client.fetch(url,method='GET')
            #print response.body
            html = response.body if isinstance(response.body, str) else response.body.decode()
            #print html
            data=json.loads(html)['data']
            userid=data['user_id']
            ip=data['ip']
            containid=data['container_id'][:12]
        except Exception,e:
            loger.log(50, 'Add_Agent:Exception %s' % e)
            self.write(json.dumps({'version':version,'data':'','error': {"error_message": '%s' % e, "error_code": "500"}
                        }) )
        if domain=='null' or monitor_params=='null':
            loger.log(50, 'Add_Agent:domain is null')
            
            self.write(json.dumps({'version':version,'data':'','error': {"error_message": 'less parameter', "error_code": "500"}
                                   }) )
        else:
            try:
                
                #dockerM(Session).add_agent(ip, 255)
                loger.log(20, 'ip:%s,userid:%s,containid:%s' % (ip,userid,containid))
                for i in  monitor_params.split('$'):
                    type1,threshold1,status=i.split(':')
                    
                    dockerM(Session).defineMonitor(ip, containid, type1, userid, domain, threshold1, status1=status)
                        
                self.write(json.dumps({'version':version,'data':{"STATUS": "success"},'error': {"error_message": "success", "error_code": "200"}
                                   }) )
            except Exception,e:
                loger.log(50, 'Add_Agent:Exception %s' % e)
                self.write(json.dumps({'version':version,'data':'','error': {"error_message": '%s' % e, "error_code": "500"}
                                   }) )
            finally:
                Session.close_all()

class Get_Default(tornado.web.RequestHandler):
    def get(self):
        try:
            result=Session.query(template.template_id,template.items,template.threshold).filter(template.template_id!=10).all()
            #print result
            #Session.commit()
            version=get_version()
            print version
            data=[]
            
            for i in result:
                data.append({'id':i.template_id,'items':i.items,'threshold':i.threshold})
            loger.log(20, 'Get_Moinitor_Info:ok')
            self.write(json.dumps({'version':version,'data':data,'error': {"error_message": "success", "error_code": "200"}
                                   }) )
        except Exception,e:
            loger.log(50, 'Get_Moinitor_Info:Exception %s' % e)
            self.write(json.dumps({'version':version,'data':'','error': {"error_message": '%s' % e, "error_code": "500"}
                                   }) )
            
        finally:
            Session.close_all()

class Get_Moinitor_Info(tornado.web.RequestHandler):
    def get(self):
        monitorid=self.get_argument('monitor_id','null')
        print monitorid
        
        if monitorid=='null' :
            loger.log(50, 'Get_Moinitor_Info:monitor_id is null')
            self.write(json.dumps({'status':'err','action':'get_monitor_info','detail':'no monitor_id'}))
        else:
            try:
                result=Session.query(monitor).filter(monitor.monitor_id==monitorid).all()
                print result
                #Session.commit()
                loger.log(20, 'Get_Moinitor_Info:ok')
                self.write(json.dumps(result, cls=new_alchemy_encoder(), check_circular=False) )
            except Exception,e:
                loger.log(50, 'Get_Moinitor_Info:Exception %s' % e)
                self.write(json.dumps({'status':'err','action':'get_monitor_info','detail':'%s' % e}))
            finally:
                Session.close_all()
                
class create_basetemplate(tornado.web.RequestHandler):
    def get(self):
        try:
            dockerM(Session).BaseTemplate()
            loger.log(20, 'create_basetemplate:ok')
            self.write(json.dumps({'status':'ok','action':'create_baseTemplate'}))
        except Exception,e:
            loger.log(50, 'create_basetemplate:Exception %s' % e)
            self.write(json.dumps({'status':'err','action':'update_monitor','detail':'%s' % e}))
        finally:
                Session.close_all()

            
            
class Monitor_List_By_User(tornado.web.RequestHandler):
    def get(self):
        userid=self.get_argument('user_id','null')
        
        
        if userid=='null' :
            loger.log(50, 'Monitor_List_By_User:userid is null')
            self.write(json.dumps({'status':'err','action':'list_monitor','detail':'no userid'}))
        else:
            try:
                result=Session.query(monitor).filter(monitor.user_id==userid).all()
                loger.log(20, 'Monitor_List_By_User:ok')
                self.write(json.dumps(result, cls=new_alchemy_encoder(), check_circular=False))
            except Exception,e:
                loger.log(50, 'Monitor_List_By_User:Exception %s' % e)
                self.write(json.dumps({'status':'err','action':'list_monitor','detail':'%s' % e}))
            finally:
                Session.close_all()

