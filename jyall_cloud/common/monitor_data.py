#coding=utf-8
'''
Created on Mar 22, 2016

@author: root
'''

import tornado.web
from jyall_cloud.utils.logging_tools import getlog
from jyall_cloud.base.dbsession import DBSession
from jyall_cloud.base.model import *


Session=DBSession

class Get_Monitor_By_time(tornado.web.RequestHandler):
    def post(self):
        monitorid=self.get_argument('monitor_id','null')
        user_id=self.get_argument('user_id','null')
        time=self.get_argument('time','null')
        start_time=self.get_argument('start_time','null')
        end_time=self.get_argument('end_time','null')
        #print monitor_id,user_id,time,start_time,end_time
        
        if monitorid=='null' or user_id=='null' or time=='null' or start_time=='null' or end_time=='null':
            
            self.write('error')
        else:
            type=Session.query(monitor.type,monitor.status).filter(monitor.monitor_id==monitorid).first()
            '''if type.status==1:
                if type in [4,6,8,9]:
                    result=Session.query().filter(history_sys.monitor_id==monitorid,history_sys.time.between(start_time - end_time).all()
                elif type ==3:
                    print 2
                else:
                    print 3'''
                
            self.write('monitor data')
        
class Get_Laster_item(tornado.web.RequestHandler):
    def post(self):
        monitor_id=self.get_argument('monitor_id','null')
        user_id=self.get_argument('user_id','null')
        time=self.get_argument('time','null')
        
        print monitor_id,user_id,time
        
        if monitor_id=='null' or user_id=='null' or time=='null':
            self.write('error')
        else:
            self.write('laster monitor data')

class Get_Monitor_Recent_Date(tornado.web.RequestHandler):
    def post(self):
        monitor_id=self.get_argument('monitor_id','null')
        user_id=self.get_argument('user_id','null')
        time=self.get_argument('time','null')
        duration=self.get_argument('duration','null')
        
        print monitor_id,user_id,time,duration
        
        if monitor_id=='null' or user_id=='null' or time=='null' or duration=='null':
            self.write('error')
        else:
            self.write(monitor_id + user_id + time + duration)

class Get_Moinitor_Status(tornado.web.RequestHandler):
    def post(self):
        monitor_id=self.get_argument('monitor_id','null')
        user_id=self.get_argument('user_id','null')
        time=self.get_argument('time','null')
        
        print monitor_id,user_id,time
        
        if monitor_id=='null' or user_id=='null' or time=='null':
            self.write('error')
        else:
            self.write(monitor_id + user_id + time )

class Get_Monitor_By_DC(tornado.web.RequestHandler):
    def post(self):
        docker_id=self.get_argument('docker_id','null')
        user_id=self.get_argument('user_id','null')
        time=self.get_argument('time','null')
        
        print docker_id,user_id,time
        
        if docker_id=='null' or user_id=='null' or time=='null':
            self.write('error')
        else:
            self.write(docker_id + user_id + time )








