#!/usr/bin/env python
#-*- coding:utf-8


''' 
程序日志封装类
记录程序文本操作流程

	@初始化/自定义写入文本名称 LOGGING_INIT(filename)
	@支持函数引用/退出 日志记录
	@支持INFO WARNING ERROR DEBUG自定义日志记录 GERROR('ERROR')
	@支持错误/异常 调用日志写入
	@TAB格式优化展示
	@输入变量/多变量 记录日志


Author: li.yan@jyall.com 

History:
	2015-12-25:
		(+)根据tornado的log.py做了进一步的修改


TODO:
	@添加DEBUG模式 支持调用函数DEBUG输出在终端





'''

import logging
import inspect

class LogLevels(object):

    INFO    = "[INFO   ]"
    WARNING = "[WARNING]"
    ERROR   = "[ERROR  ]"
    DEBUG   = "[DEBUG  ]"


class Log(object):
	'''
	基本Log类
	'''
	def __init__(self, fn):

		super(Log, self).__init__()
		self.__tab_count = 0
		self.logger = logging.getLogger( __name__ )
		self.logger.setLevel(logging.INFO)

		#file handler
		self.fh = logging.FileHandler(fn, mode='a+')
		self.fh.setLevel(logging.INFO)
		formatter  = logging.Formatter('[%(asctime)s] %(message)s')
		self.fh.setFormatter(formatter)
		self.logger.addHandler(self.fh)

	def __log(self, level, message, *args):

		log_params = self.__get_params(*args)
		self.logger.info("{lev}: {tabs}{message}{params}".format(lev = level, tabs=' '*self.__tab_count, message = message, params=log_params))



	#INFO WARNING ERROR DEBUG自定义日志记录
	def info(self, message, *args):
		self.__log(LogLevels.INFO, message, *args)
	def warning(self, message, *args):
		self.__log(LogLevels.WARNING, message, *args)
	def error(self, message, *args):
		self.__log(LogLevels.ERROR, message, *args)
	def debug(self, message, *args):
		self.__log(LogLevels.DEBUG, message, *args)

	def log_param(self, name_param, param):

		'''单变量记录'''
		self.info("%s=[%s]" %(name_param, param))

	def log_params(self, *args):

		'''多变量记录'''
		self.info("", *args)


	# 函数引用/退出信息
	def enter_func(self, *args):

		cl_fn = self.__get_class_func()
		l_params = self.__get_params(*args)
		self.info("Enter: %s%s" %(cl_fn , l_params))
		self.__inc_tabs()

	def leave_func(self):
		self.__dec_tabs()
		cl_fn = self.__get_class_func()
		self.info("Leave: %s" %cl_fn)

    
	def call_func_error(self, func_name, res):

		'''
		调用失败 异常错误处理记录
		'''
		line_num = inspect.currentframe().f_back.f_back.f_lineno

		self.error("failed: %s, res=%s, line=%s" %(func_name, res, line_num))

		self.__dec_tabs()

		cl_fn = self.__get_class_func()
		self.error("Leave: %s - failed" % cl_fn)

	def leave_func_error(self, cond, *args):
		l_params = self.__get_params(*args)

		line_num = inspect.currentframe().f_back.f_back.f_lineno
		self.error("failed: '%s', line=%s%s" %(cond, line_num, l_params))

		self.__dec_tabs()
		cl_fn = self.__get_class_func()
		self.error("Leave: %s - failed" % cl_fn)


	
	def __get_class_func(self):

		fn = inspect.currentframe().f_back.f_back.f_back

		classname = ""
		funcname = fn.f_code.co_name
		args, _, _, value_dict = inspect.getargvalues(fn)
		if len(args) and args[0] == 'self':
			instance = value_dict.get('self', None)
			if instance:
				ga = getattr(instance, '__class__', None)
				classname = ga.__name__

		return "%s::%s" %(classname, funcname)

	def __get_params(self, *args):

		if not args:
			return ""
		i=0
		params = ""
		for arg in args:
			i+=1
			params += ", ARG.%i=[%s]" %(i,arg)
		return params

	def __g_tabs(self):
		return ' '*self.__tab_count

	def __inc_tabs(self):
		self.__tab_count+=2

	def __dec_tabs(self):
		self.__tab_count-=2





LOGQ = Log


def LOGGING_INIT(filename):

	'''
	初始化函数
	'''


	global LOGQ
	LOGQ = Log(filename)


def FUNC_START(*args):

	'''
	函数标识,调用函数
	'''
	LOGQ.enter_func(*args)

def FUNC_EXIT_SUCCESS():

	'''
	正常退出函数
	'''

	LOGQ.leave_func()

def FUNC_CALL_ERROR(func_name, res):

	'''
	异常调用
	'''

	LOGQ.call_func_error(func_name, res)

def FUNC_EXIT_ERROR(cond, *args):

	'''
	异常调用退出
	'''
	LOGQ.leave_func_error(cond, *args)


def LOG_PARAM(param_name, param):

	'''
	单变量记录
	'''
	LOGQ.log_param(param_name, param)

def LOG_PARAMS(*args):

	'''
	多变量记录
	'''
	LOGQ.log_params(*args)



def GINFO(message, *args):

	'''INFO记录'''

	LOGQ.info(message, *args)

def GWARN(message, *args):

	'''WARNING记录'''

	LOGQ.warning(message, *args)

def GERROR(message, *args):

	'''ERROR记录'''

	LOGQ.error(message, *args)

def GDEBUG(message, *args):

	'''DEBUG记录'''

	LOGQ.debug(message, *args)


