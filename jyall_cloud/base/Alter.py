from model import *

class Alter(object):
    def __init__(self,userid,containid,session,):
        self.result={}
        self.user_id=userid
        self.Session=session
        self.containid=containid
    
    def net(self):
         
        if self.Session.query(monitor).\
            filter(monitor.user_id==self.user_id,monitor.type=='3',monitor.container_id==self.containid,monitor.status==1).\
            first()!=None:
            m=self.Session.query(monitor).\
            filter(monitor.user_id==self.user_id,monitor.type=='3',monitor.container_id==self.containid,monitor.status==1).\
            first()
            
            
            a=self.Session.query((history_net.rx_bytes+history_net.tx_bytes).label('total')).\
            filter(history_net.monitor_id==m.monitor_id).\
            order_by(history_net.time.desc()).limit(5).all()
            
            r=0
            for i in a:
                i=i[0]
                r=r+i
            avg=r/5
            #print avg
            if int(avg/1024/1024) < int(m.threshold):
                self.result['netTraffic']='ok'
            else:
                self.result['netTraffic']='err'
                err=self.Session.query(monitor.agent_id,monitor.email).filter(monitor.user_id==self.user_id,monitor.type=='3',monitor.container_id==self.containid).first()
                alternet=alert(agent_id=err.agent_id,
                               contain_id=self.containid,
                               alert_email=err.email)
                self.Session.add(alternet)
                self.Session.commit()
            print 'net'
    def cpu(self):
        
        if self.Session.query(monitor).\
            filter(monitor.user_id==self.user_id,monitor.type=='1',monitor.container_id==self.containid,monitor.status==1).\
            first()!=None:
            
            m=self.Session.query(monitor).\
            filter(monitor.user_id==self.user_id,monitor.type=='1',monitor.container_id==self.containid,monitor.status==1).\
            first()
    
            
            a=self.Session.query((history_sys.value).label('total')).\
            filter(history_sys.monitor_id==m.monitor_id).\
            order_by(history_sys.time.desc()).limit(5).all()
            
            r=0
            for i in a:
                
                i=float(i[0])
                r=r+i
            avg=r/5
            if float(avg*100) < float(m.threshold):
                #print a.avg*100
                self.result['cpu']='ok'
            else:
                self.result['cpu']='err'
                err=self.Session.query(monitor.agent_id,monitor.email).filter(monitor.user_id==self.user_id,monitor.type=='1',monitor.container_id==self.containid).first()
                alternet=alert(agent_id=err.agent_id,
                               contain_id=self.containid,
                               alert_email=err.email)
                self.Session.add(alternet)
                self.Session.commit()
        print 'cpu'    
    def iowait(self):
        if self.Session.query(monitor).\
        filter(monitor.user_id==self.user_id,monitor.type=='2',monitor.container_id==self.containid,monitor.status==1).\
        first()!=None:
            m=self.Session.query(monitor).\
            filter(monitor.user_id==self.user_id,monitor.type=='2',monitor.container_id==self.containid,monitor.status==1).\
            first()
            #print m
            
            a=self.Session.query((history_sys.value).label('total')).\
            filter(history_sys.monitor_id==m.monitor_id).\
            order_by(history_sys.time.desc()).limit(5).all()
            
            r=0
            for i in a:
                i=float(i[0])
                r=r+i
            avg=r/5
            if float(avg*100) < float(m.threshold):
                self.result['iowait']='ok'
            else:
                self.result['iowait']='err'
                err=self.Session.query(monitor.agent_id,monitor.email).filter(monitor.user_id==self.user_id,monitor.type=='2',monitor.container_id==self.containid).first()
                alternet=alert(agent_id=err.agent_id,
                               contain_id=self.containid,
                               alert_email=err.email)
                self.Session.add(alternet)
                self.Session.commit()
            print 'iow'
    def mem(self):
        if self.Session.query(monitor).\
        filter(monitor.user_id==self.user_id,monitor.type=='5',monitor.container_id==self.containid,monitor.status==1).\
        first()!=None:
            m=self.Session.query(monitor).\
            filter(monitor.user_id==self.user_id,monitor.type=='5',monitor.container_id==self.containid,monitor.status==1).\
            first()
    
            
            a=self.Session.query((history_sys.value).label('total')).\
            filter(history_sys.monitor_id==m.monitor_id).\
            order_by(history_sys.time.desc()).limit(5).all()
            
            r=0
            for i in a:
                i=float(i[0])
                r=r+i
            avg=r/5
            #print float(a.avg*100) 
            if float(avg*100) < float(m.threshold):
                self.result['mem']='ok'
            else:
                self.result['mem']='err'
                err=self.Session.query(monitor.agent_id,monitor.email).filter(monitor.user_id==self.user_id,monitor.type=='5',monitor.container_id==self.containid).first()
                alternet=alert(agent_id=err.agent_id,
                               contain_id=self.containid,
                               alert_email=err.email)
                self.Session.add(alternet)
                self.Session.commit()
            print 'mem'
    def df(self):
        if self.Session.query(history_sys.list,monitor.threshold).join(monitor).\
            filter(monitor.user_id==self.user_id,monitor.type=='6',monitor.container_id==self.containid,monitor.status==1).\
            order_by(history_sys.time.desc()).first()!=None:
            a=self.Session.query(history_sys.list,monitor.threshold).join(monitor).\
            filter(monitor.user_id==self.user_id,monitor.type=='6',monitor.container_id==self.containid,monitor.status==1).\
            order_by(history_sys.time.desc()).first()
            
            w11=dict(eval(a[0]))
            df={}
            err=self.Session.query(monitor.agent_id,monitor.email).filter(monitor.user_id==self.user_id,monitor.type=='6',monitor.container_id==self.containid).first()
            for i in w11.keys():
                if int(w11[i]['UsePercent']) > int(a[1]):
                    df[i]='err'
                    alternet=alert(agent_id=err.agent_id,
                               contain_id=self.containid,
                               alert_email=err.email)
                    self.Session.add(alternet)
                    self.Session.commit()
                else:
                    df[i]='ok'
            self.result['df']=df
            
            
    def io(self):
        if self.Session.query(monitor).\
            filter(monitor.user_id==self.user_id,monitor.type=='7',monitor.container_id==self.containid,monitor.status==1).\
            first()!=None:
            m=self.Session.query(monitor).\
            filter(monitor.user_id==self.user_id,monitor.type=='7',monitor.container_id==self.containid,monitor.status==1).\
            first()
    
            
            a=self.Session.query((history_io.total).label('total')).\
            filter(history_io.monitor_id==m.monitor_id).\
            order_by(history_io.time.desc()).limit(5).all()
            print a
            r=0
            for i in a:
                i=float(i[0])
                r=r+i
            avg=r/5
            if int(avg/1024/1024) < int(m.threshold):
                self.result['io']='ok'
            else:
                self.result['io']='err'
                err=self.Session.query(monitor.agent_id,monitor.email).filter(monitor.user_id==self.user_id,monitor.type=='7',monitor.container_id==self.containid).first()
                alternet=alert(agent_id=err.agent_id,
                               contain_id=self.containid,
                               alert_email=err.email)
                self.Session.add(alternet)
                self.Session.commit()
    def proc(self):
        import re
        if self.Session.query(history_sys.list,monitor.threshold).join(monitor).\
                    filter(monitor.user_id==self.user_id,monitor.type=='8',monitor.container_id==self.containid,monitor.status==1).\
                    order_by(history_sys.time.desc()).first()!=None:
            a=self.Session.query(history_sys.list,monitor.threshold).join(monitor).\
                    filter(monitor.user_id==self.user_id,monitor.type=='8',monitor.container_id==self.containid,monitor.status==1).\
                    order_by(history_sys.time.desc()).first()
            reproc=re.compile('\w\W+%s\w\W+' % a.threshold)
            print a.threshold
            for i in  dict(eval(a.list)):
                print i
                self.result['proc']='err'
                if reproc.search(i):
                    self.result['proc']='ok'
                if self.result['proc']=='err':
                    err=self.Session.query(monitor.agent_id,monitor.email).filter(monitor.user_id==self.user_id,monitor.type=='8',monitor.container_id==self.containid).first()
                    alternet=alert(agent_id=err.agent_id,
                               contain_id=self.containid,
                               alert_email=err.email)
                    self.Session.add(alternet)
                    self.Session.commit()
                
                    
    def port(self):
        import re
        if self.Session.query(history_sys.list,monitor.threshold).join(monitor).\
                filter(monitor.user_id==self.user_id,monitor.type=='9',monitor.container_id==self.containid,monitor.status==1).\
                order_by(history_sys.time.desc()).first()!=None:
            a=self.Session.query(history_sys.list,monitor.threshold).join(monitor).\
                filter(monitor.user_id==self.user_id,monitor.type=='9',monitor.container_id==self.containid,monitor.status==1).\
                order_by(history_sys.time.desc()).first()
            #print a
            self.result['port']='err' 
            for i in  dict(eval(a.list)):
                i=i.split(':')[1]
                #print i ,a.threshold
                if int(i)==int(a.threshold):
                    self.result['port']='ok'
                if self.result['port']=='err':
                    err=self.Session.query(monitor.agent_id,monitor.email).filter(monitor.user_id==self.user_id,monitor.type=='9',monitor.container_id==self.containid).first()
                    alternet=alert(agent_id=err.agent_id,
                               contain_id=self.containid,
                               alert_email=err.email)
                    self.Session.add(alternet)
                    self.Session.commit()
                           
            print 'port'
    def main(self):
        self.net()
        self.cpu()
        self.io()
        self.iowait()
        self.mem()
        self.df()
        self.port()
        self.proc()
        self.result['id']=self.containid
        self.Session.close_all()
        return self.result
