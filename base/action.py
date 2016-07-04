#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from base.user import User
from base.tieba import Tieba


__author__ = 'palle'

def guanzhu_test():
	user = User('用户名', '密码', )
	user.login()
	tiebalist = ['lol', 'dnf', 'cf', 'python', 'unity3d', 'ue4', '天涯明月刀OL', '李毅', '魔兽世界', '美女', '魔兽玩家', 'java', 'c++',
				 '动漫', '冒险岛2', '暗黑3', '激战2']

	for tiebaname in tiebalist:
		tieba = Tieba(tiebaname)
		tieba.guanzhu(user)

def qiandao_test():
	user = User('用户名', '密码', )
	user.login()
	tiebalist = ['lol', 'dnf', 'cf', 'python', 'unity3d', 'ue4', '天涯明月刀OL', '李毅', '魔兽世界', '美女', '魔兽玩家', 'java', 'c++',
				 '动漫', '冒险岛2', '暗黑3', '激战2']

	for tiebaname in tiebalist:
		tieba = Tieba(tiebaname)
		tieba.qiandao(user)

def onkeyqiandao_test():
	user = User('用户名', '密码', )
	user.login()
	tieba = Tieba('暗黑3')
	tieba.onekey_qiandao(user)

def fatie_test():
	user = User('用户名', '密码', )
	user.login()
	tieba = Tieba('寻找女王控')
	tieba.fatie(user)

def huitie_test():
	user = User('用户名', '密码', )
	user.login()
	tieba = Tieba('寻找女王控')
	tiezi_url='http://tieba.baidu.com/p/4479248232'
	tieba.huitie(user,tiezi_url)

if __name__ == '__main__':
	huitie_test()
