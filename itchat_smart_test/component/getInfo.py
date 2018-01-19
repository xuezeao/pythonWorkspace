# -*- coding:utf-8 -*-

import itchat
from itchat.content import *
import requests

USERNAME = ""
Friends_Enable = ["ags-陈思思"]
Group_Enable = [""]

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': '87e4a4b7dcfa42e3868aa9de0ef91ce6',  # Tuling Key
        'info': msg,  # 这是我们发出去的消息
        'userid': 'wechat-robot',  # 这里你想改什么都可以
    }
    # 我们通过如下命令发送一个post请求
    r = requests.post(apiUrl, data=data).json()
    return r.get('text')

#用于筛选个人私聊对象
@itchat.msg_register(TEXT, isFriendChat=True)
def print_info(msg):
    #过滤用户本身信息
    if msg['FromUserName'] == USERNAME:
        return print("the message is my")
    #识别信息内容
    try:
        __USERNAME = msg['User']['RemarkName']
        print("sender Name : %s" % __USERNAME)
    except:
        print("sender Name : %s" % msg['ToUserName'])
        print("info: %s" % msg['Text'])
        return
    print(msg)
    if not division_primet(__USERNAME):
        return print("ignore--------")
    else:
        print("I received: %s" % msg['Text'])

    return get_response(msg['Text'])

#用于接收群的文字信息
@itchat.msg_register(TEXT, isGroupChat=True)
def print_info_G(msg):
        #过滤用户本身信息
        if msg['FromUserName'] == USERNAME :
            return print("the message is my")
        #过滤非允许对象信息
        try:
            __FromInfoGroup = msg['User']['NickName']
            print("-----received one info -----------")
            print("GroupName: %s " % msg['User']['NickName'])
            #如果没从允许列表中找到则不显示消息的内容
            Group_Enable.index(__FromInfoGroup)
        except:
            return print("this group isn't enable list...")

        print("-------------GroupReceivedInfo------------")
        print("is @ me: %s" % msg.isAt)
        print("said name: %s " % msg.actualNickName)
        print("said Text: %s " % msg.text)
        return get_response(msg['Text'])

def division_primet(userName):
    userName = userName
    try:
        Friends_Enable.index(userName)
    except:
        print("this people have not permit: %s" % userName)
        return False
    return True


if __name__ == '__main__':

    itchat.auto_login(True)
    #获取用户本身ID，在后续程序中剔除
    tempUser = itchat.search_friends()
    USERNAME = tempUser['UserName']
    print("hello, %s" % tempUser['NickName'])

    #循环执行
    itchat.run(True)


