#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import requests
import re
from base.user import User
from PIL import Image
from io import BytesIO
import time

__author__ = 'palle'

def str2dic(text):
	idic ={}
	ilist = text.split('&')
	for item in ilist:
		name,value = item.split('=',1)
		idic[name] = value
	return idic


class Tieba(object):
	guanzhu_url = 'http://tieba.baidu.com/f/like/commit/add'
	guanzhu_data_text = 'fid=2705621&fname=%E5%AF%BB%E6%89%BE%E5%A5%B3%E7%8E%8B%E6%8E%A7&uid=%25E5%25A0%2595%25E5%25A4%25A9%25E4%25BD%25BF%25E8%25B4%259D%25E5%2588%25A9%25E5%25B0%2594%26ie%3Dutf-8&ie=gbk&tbs=e6f56e1ed5b837701460516650'
	guanzhu_data = str2dic(guanzhu_data_text)
	qiandao_url = 'http://tieba.baidu.com/sign/add'
	onkeyqiandao_url = 'http://tieba.baidu.com/tbmall/onekeySignin1'
	def __init__(self,tiebaname):
		self.tieba_name = tiebaname
		self.tieba_url = 'http://tieba.baidu.com/f'

	#获取贴吧界面text
	def get_tieba_text(self,user):
		data={}
		data['kw']=self.tieba_name
		res = requests.get(self.tieba_url, params=data,cookies=user.Cookies())
		self._tiebatext = res.text
		# print(res.url)

	#获取fid和tbs
	def get_fid_and_tbs(self,text):
		patternTBS1 = re.compile("'tbs': (.*?)    };")
		patternTBS2 = re.compile("'tbs':'(.*?)'")
		patternTBS3 = re.compile('"tbs": "(.*?)",')
		_tbs = ''
		if _tbs=='':
			if not len(re.findall(patternTBS1, text)) ==0:
				_tbs = re.findall(patternTBS1, text)[0]
		if _tbs=='':
			if not len(re.findall(patternTBS2, text)) ==0:
				_tbs = re.findall(patternTBS2, text)[0]
		if _tbs=='':
			if not len(re.findall(patternTBS3, text)) ==0:
				_tbs = re.findall(patternTBS3, text)[0]

		patternFID = re.compile('"forum_id":(\d+),')
		if not len(re.findall(patternFID,text)) == 0:
			_fid = re.findall(patternFID,text)[0]
		else:
			print('获取FID数据失败')
			_fid = ''
		return _fid,_tbs
	#构建关注post数据
	def create_guanzhu_commit_data(self,user):
		self.get_tieba_text(user)
		patternTBS1 = re.compile("'tbs': (.*?)    };")
		patternTBS2 = re.compile("'tbs':'(.*?)'")
		# self.guanzhu_data['tbs'] = re.findall(patternTBS1,self._tiebatext)
		if len(re.findall(patternTBS1,self._tiebatext)) == 0:
			if len(re.findall(patternTBS2,self._tiebatext)) == 0 :
				print('{}关注失败111'.format(self.tieba_name))
			else:
				self.guanzhu_data['tbs'] = re.findall(patternTBS2, self._tiebatext)[0]
		else:
			self.guanzhu_data['tbs'] = re.findall(patternTBS1, self._tiebatext)[0].strip('"')
		patternFID = re.compile('"forum_id":(\d+),')
		if not len(re.findall(patternFID,self._tiebatext)) == 0:
			self.guanzhu_data['fid'] = re.findall(patternFID,self._tiebatext)[0]
		self.guanzhu_data['fname'] = self.tieba_name
		self.guanzhu_data['uid'] = user.Name()
	#关注贴吧
	def guanzhu(self,user):
		self.create_guanzhu_commit_data(user)
		# print(self.guanzhu_data)
		# print(user.Cookies())
		res = requests.post(self.guanzhu_url,data=self.guanzhu_data,cookies=user.Cookies())
		# print(res.text)
		self.check_guanzhu_result(res.text)
	#检查是否关注成功
	def check_guanzhu_result(self,text):
		pattern = re.compile('"no":(\d+)')
		result = int(re.findall(pattern,text)[0])
		if result == 0:
			print('{}吧关注成功'.format(self.tieba_name))
		elif result == 221:
			print('{}吧已经被关注过'.format(self.tieba_name))
		else:
			print('{}吧关注失败'.format(self.tieba_name))

	#单个贴吧签到
	def qiandao(self,user):
		data={}
		data['ie'] = 'utf-8'
		data['kw'] = self.tieba_name

		self.get_tieba_text(user)
		patternTBS1 = re.compile("'tbs': (.*?)    };")
		patternTBS2 = re.compile("'tbs':'(.*?)'")
		if len(re.findall(patternTBS1, self._tiebatext)) == 0:
			if len(re.findall(patternTBS2, self._tiebatext)) == 0:
				data['tbs']=''
				print('{}吧tbs没找到'.format(self.tieba_name))
			else:
				data['tbs']= re.findall(patternTBS2, self._tiebatext)[0]
		else:
			data['tbs'] = re.findall(patternTBS1, self._tiebatext)[0].strip('"')

		res = requests.post(self.qiandao_url, data=data, cookies=user.Cookies())
		print(res.text)

		pattern = re.compile('"no":(\d+)')
		result = int(re.findall(pattern, res.text)[0])
		if result == 0:
			print('{}吧签到成功'.format(self.tieba_name))
		elif result == 1101:
			print('你在{}吧已经签到过了'.format(self.tieba_name))
		else:
			print('{}吧签到失败'.format(self.tieba_name))

	#一键签到功能
	def onekey_qiandao(self,user):
		data = {}
		data['ie'] = 'utf-8'

		res = requests.get('http://tieba.baidu.com/',cookies=user.Cookies())
		patternTBS = re.compile("'tbs':'(.*?)'}")
		data['tbs'] = re.findall(patternTBS, res.text)[0]

		res = requests.post(self.onkeyqiandao_url, data=data, cookies=user.Cookies())
		pattern = re.compile('"no":(\d+)')
		result = int(re.findall(pattern, res.text)[0])
		if result == 0:
			print('一键签到成功')
		else:
			print('一键签到失败')

	#发帖
	def fatie(self,user):
		fatie_data_text='ie=utf-8&kw=%E5%AF%BB%E6%89%BE%E5%A5%B3%E7%8E%8B%E6%8E%A7&fid=2705621&tid=0&vcode_md5=&floor_num=0&rich_text=1&tbs=006b0762828f53551460598534&content=%E8%BF%99%E9%87%8C%E6%98%AF%E5%86%85%E5%AE%B9&title=%E8%BF%99%E9%87%8C%E6%98%AF%E4%B8%BB%E9%A2%98&prefix=&files=%5B%5D&mouse_pwd=87%2C83%2C80%2C78%2C83%2C87%2C91%2C87%2C107%2C83%2C78%2C82%2C78%2C83%2C78%2C82%2C78%2C83%2C78%2C82%2C78%2C83%2C78%2C82%2C78%2C83%2C78%2C82%2C107%2C86%2C82%2C84%2C85%2C83%2C107%2C83%2C91%2C80%2C82%2C78%2C83%2C82%2C90%2C82%2C14605984952980&mouse_pwd_t=1460598495298&mouse_pwd_isclick=0&__type__=thread'
		fatie_data = str2dic(fatie_data_text)
		self.get_tieba_text(user)
		fatie_data['fid'],fatie_data['tbs'] = self.get_fid_and_tbs(self._tiebatext)
		fatie_data['kw'] = self.tieba_name
		zhuti = 'post发帖主题'+ str(time.time())
		neirong = 'post发帖内容' + str(time.time())
		fatie_data['title'] = zhuti
		fatie_data['content'] = neirong

		res = requests.post('http://tieba.baidu.com/f/commit/thread/add',cookies=user.Cookies(),data=fatie_data)
		# print(res.text)
		pattern_check = re.compile('"no":(.*?),')
		check_num = int(re.findall(pattern_check, res.text)[0])
		print(check_num)
		if check_num == 0:
			pattern = re.compile('"tid":(\d+),')
			tid = re.findall(pattern, res.text)[0]
			# print(tid)
			tiezi_url = 'http://tieba.baidu.com/p/' + tid
			print('发帖成功，帖子地址为：' + tiezi_url)
		elif check_num == 40:
			pattern_vcode = re.compile('"captcha_vcode_str":"(.*?)"')
			vcode_data = re.findall(pattern_vcode,res.text)[0]
			data = {'tag':'pc','t':''}

			vcodeimgdata = requests.get('http://tieba.baidu.com/cgi-bin/genimg?'+vcode_data,cookies = user.Cookies(),data=data)
			# print(vcodeimgdata.content)
			vcode_img = Image.open(BytesIO(vcodeimgdata.content))
			vcode_img.save('vcode_img.png')

			# fatie_data['vcode_md5'] = vcode_data
			# #每8个字符代表一个字，前4字符为列，后4字符为行
			# fatie_data['vcode'] = '00000001000100000001000100020001'
			# #带验证码发帖
			# requests.post('http://tieba.baidu.com/f/commit/thread/add', cookies=user.Cookies(), data=fatie_data)
			# pattern_check = re.compile('"no":(.*?),')
			# check_num = int(re.findall(pattern_check, res.text)[0])
			# print(check_num)
			# if check_num == 0:
			# 	pattern = re.compile('"tid":(\d+),')
			# 	tid = re.findall(pattern, res.text)[0]
			# 	print(tid)
			# 	tiezi_url = 'http://tieba.baidu.com/p/' + tid
			# 	print('发帖成功，帖子地址为：' + tiezi_url)
	#回帖
	def huitie(self,user,url):
		huitie_data_text = 'ie=utf-8&kw=%E5%AF%BB%E6%89%BE%E5%A5%B3%E7%8E%8B%E6%8E%A7&fid=2705621&tid=4479203767&vcode_md5=&floor_num=1&rich_text=1&tbs=4738ba81c14d48621460608375&content=%E5%9B%9E%E5%B8%96%E7%9A%84%E5%86%85%E5%AE%B9&files=%5B%5D&mouse_pwd=41%2C44%2C43%2C48%2C45%2C46%2C47%2C40%2C21%2C45%2C48%2C44%2C48%2C45%2C48%2C44%2C48%2C45%2C48%2C44%2C48%2C45%2C48%2C44%2C48%2C45%2C48%2C44%2C21%2C37%2C42%2C41%2C43%2C40%2C21%2C45%2C37%2C46%2C44%2C48%2C45%2C44%2C36%2C44%2C14606083214280&mouse_pwd_t=1460608321428&mouse_pwd_isclick=0&__type__=reply'
		huitie_data = str2dic(huitie_data_text)

		res = requests.get(url,cookies=user.Cookies())
		# print(res.text)
		huitie_data['fid'],huitie_data['tbs'] = self.get_fid_and_tbs(res.text)
		# print(huitie_data['tbs']+'____'+huitie_data['fid'])
		huitie_data['kw'] = self.tieba_name
		pattern = re.compile('reply_num:(\d+),')
		huitie_data['floor_num'] = re.findall(pattern,res.text)[0]
		print(huitie_data['floor_num'])
		huitie_data['tid'] = url.split('/p/',1)[1]
		huitie_data['mouse_pwd_t'] = str(math.floor(time.time()*1000))
		huitie_data['mouse_pwd'] = '2,2,12,24,5,3,2,4,61,5,24,4,24,5,24,4,24,5,24,4,24,5,24,4,24,5,24,4,61,5,13,0,12,12,4,61,5,13,6,4,24,5,4,12,4,'+huitie_data['mouse_pwd_t']+'0'

		biaoqing='[emotion pic_type=1 width=30 height=30]http://tb2.bdstatic.com/tb/editor/images/face/i_f03.png?t=20140803[/emotion]'
		neirong = biaoqing+str(time.time())
		huitie_data['content'] = neirong


		print(huitie_data)


		headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36','Referer': 'http://tieba.baidu.com/p/4479216985'}

		res = requests.post('http://tieba.baidu.com/f/commit/post/add',data=huitie_data,headers=headers,cookies=user.Cookies())
		print(res.text)
		pattern_check = re.compile('"no":(.*?),')
		check_num = int(re.findall(pattern_check, res.text)[0])
		print(check_num)
		if check_num == 0:
			pattern = re.compile('"content":"(.*?)",')
			content = re.findall(pattern, res.text)[0]
			print('回帖成功，回复内容为：' + content)
		elif check_num == 40:
			print('回帖失败，需要验证码')
		else:
			print('回帖失败')
	#楼中楼回复
	def louzhonglou(self):
		data_text = 'ie=utf-8&kw=lol&fid=280050&tid=4479056728&floor_num=321&quote_id=87577050793&rich_text=1&tbs=7ba37c30d3be01b31460620868&content=%E6%B5%8B%E6%B5%8B%E6%B5%8B%E6%B5%8B%E6%B5%8B%E6%B5%8B&lp_type=0&lp_sub_type=0&new_vcode=1&tag=11&repostid=87577050793&anonymous=0'
		data = str2dic(data_text)
		print(data)

	#私信
	def fasixin(self):
		pass
	#点赞
	def dianzan(self):
		pass
	#获取贴吧成员
	def get_tieba_member(self):
		pass
	#大召唤术
	def summon(self):
		pass
	#获取好友




if __name__ == '__main__':
	user = User('用户名','密码',)
	user.login()
	tiebalist=['lol','dnf','cf','python','unity3d','ue4','天涯明月刀OL','李毅','魔兽世界','美女','魔兽玩家','java','c++','动漫','冒险岛2','暗黑3','激战2']

	for tiebaname in tiebalist:
		tieba = Tieba(tiebaname)
		tieba.guanzhu(user)
