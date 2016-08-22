#coding = utf-8
'''
Created on Mar 29, 2016

@author: sjp
'''
import json
import urllib
from jyall_cloud.config import get_api_url

sso_url=get_api_url(api_name='authcheck')


def CheckUser(token):
    loginFlag=json.loads(urllib.urlopen(sso_url+token).read()).get('loginFlag')
    return loginFlag

#sso login api return a map object incloud tokenid 
#use tokenid to verify whether user has login
def userlogin(user,pwd):
    login_url='http://10.10.33.47/v1/authcenter/login/userLogin'
    login_info=json.loads(urllib.urlopen(login_url + '/' + user + '/' + pwd).read())
    return login_info
    
if __name__ == '__main__':
    user='15911111133'
    pwd='000000'
    userinfo=userlogin(user, pwd)
    token=userinfo.get('tokenid')
    print token
    loginFlag=CheckUser(token)
    print loginFlag
