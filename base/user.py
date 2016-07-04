#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import requests
import lxml.html
import time
import re
import random
from PIL import Image
from io import BytesIO

__author__ = 'palle'





class User(object):
	login_url = 'https://passport.baidu.com/v2/api/?login'
	token_url = 'https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true'
	check_data=''
	check_ncs_url = 'https://passport.baidu.com/v2/api/?logincheck&'

	def __init__(self,username,password,codestring=None):
		self._username = username
		self._password = password
		self._codestring = codestring
		self.check_data = 'callback=bdPass.api.login._needCodestringCheckCallback&tpl=mn&charset=UTF-8&index=0&username={}&isphone=false&time={}'.format(self._username,math.floor(time.time()*1000))
		self.check_ncs_url = self.check_ncs_url+self.check_data
		res = requests.get('http://www.baidu.com/cache/user/html/login-1.2.html')
		self._Cookies = res.cookies

	#构建登录post数据
	def _create_data(self,codestring='', verifycode=''):
		no_cs_data = {}
		datastr = 'ppui_logintime=4523396&charset=utf-8&codestring=&token=497d384be6c51ffc38bd09892957130d&isPhone=false&index=0&u=&safeflg=0&staticpage=http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html&loginType=1&tpl=mn&callback=parent.bdPass.api.login._postCallback&username=%E9%9A%90%E5%85%83%E7%A7%98%E5%AE%9D&password=12312313&verifycode=&mem_pass=on'
		datalist = datastr.split('&')
		for data in datalist:
			name, value = data.split('=', 1)
			no_cs_data[name] = value
		no_cs_data['ppui_logintime'] = random.randint(1000000, 9999999)
		no_cs_data['token'] = self._token
		no_cs_data['username'] = self._username.encode('utf-8')
		no_cs_data['password'] = self._password
		no_cs_data['codestring'] = codestring
		no_cs_data['verifycode'] = verifycode
		# print(no_cs_data)
		return no_cs_data

	#无验证码登录
	def _login_no_codestring(self):
		self._get_token()
		self.download_codestring()
		data = self._create_data()
		res = requests.post(self.login_url,data=data,cookies=self._Cookies)
		if self._check_login_success(res.text) == True:
			self._update_cookies(res.cookies)

	#有验证码登录
	def _login_codestring(self):
		self._get_token()
		verifycode = input("请输入验证码：")
		data = self._create_data(self._codestring,verifycode)
		res = requests.post(self.login_url, data=data, cookies=self._Cookies)
		if self._check_login_success(res.text) == True:
			self._update_cookies(res.cookies)

	#检查是否登录成功
	def _check_login_success(self,text):
		pattern = re.compile(r"&error=(\d+)'")
		errorcode = int(re.findall(pattern,text)[0])
		# print(errorcode)
		if errorcode == 0:
			print("登陆成功")
			return True
		elif errorcode == 1:
			print("用户名格式错误")
			return False
		elif errorcode == 2:
			print("用户不存在")
			return False
		elif errorcode == 2:
			print("密码错误")
			return False
		elif errorcode == 257:
			print("没有输入验证码")
			return False
		elif errorcode == 6:
			print("验证码输入错误")
			return False
		else:
			print("未知原因失败")
			return False

	#更新cookies
	def _update_cookies(self,cookiejar):
		self._Cookies.update(cookiejar)

	#获取token
	def _get_token(self):
		res = requests.get(self.token_url,cookies=self._Cookies)
		pattern = re.compile(r"bdPass.api.params.login_token='(.*?)';")
		self._token = re.findall(pattern, res.text)[0]
		# print(self._Cookies,res.cookies)
	#检查是否需要验证码
	def _check_need_codestring(self):
		res = requests.get(self.check_ncs_url)
		pattern = re.compile(r'"codestring":(.*?),')
		codestrings = re.findall(pattern,res.text)
		if codestrings[0] == 'null':
			return False
		else:
			self._codestring = codestrings[0]

	#下载验证码图片
	def download_codestring(self):
		# img_url = 'https://passport.baidu.com/cgi-bin/genimage?'+self._codestring
		img_url = 'https://passport.baidu.com/cgi-bin/genimage?'+'jxIcaptchaservice626261632f437071785a30715452766c2f4578743847676c394f67726a436f774c45464a676537452f644c686d444877306b364c4c4f2b4f5a2f754a33416642446955394f545851396a4c66616e6e72415a596768376836414e4f32436b377242766d6557794f636c4358747a75665034796d7077614a734264666f595a44397a704b353253726a7270556e3856394a4e767a5144775446714a4650586d6a697a5179634771324b44524441564f4c5452585a475a486a776f56784753754e495a504e586a724d4d6761687a346e436a4351624f566c474b4b726567696b7264554e7a65664d587a794c6f44576c594a554a716a73412b7550482f333342634459426c6d32414d6930716e2b344c4e4674714833694a486166655179576b75594c763631544d347377734946443770664d46543770327a75415a4277546643784a6b6b567a574a7a'
		res = requests.get(img_url,self._Cookies)
		i = Image.open(BytesIO(res.content))
		i.save('verify.jpg')

	#登录
	def login(self, *args, **kwargs):
		if self._check_need_codestring() == False:
			self._login_no_codestring()
		else:
			self._login_codestring()

	def Name(self):
		return self._username

	def Cookies(self):
		return self._Cookies



#
def test():
	res = requests.get('http://qingfengbw.cnbaowen.net/contact/')
	doc = lxml.html.fromstring(res.text)
	text = doc.xpath('//*[@align="absmddle"]')[2]
	print(text.attrib['src'])




if __name__ == '__main__':
	test()




