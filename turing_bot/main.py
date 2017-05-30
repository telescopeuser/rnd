
# coding: utf-8

# In[ ]:


import time, datetime, requests, itchat
from itchat.content import *


# In[ ]:

KEY = '71f28bf79c820df10d39b4074345ef8c'

'''
8edce3ce905a4c1dbb965e6b35c3834d
eb720a8970964f3f855d863d24406576
1107d5601866433dba9599fac1bc0083
71f28bf79c820df10d39b4074345ef8c
'''

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        print('!!! Turing Machine problem !!!')
        # 将会返回一个None
        return


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
#     print('1 on 1 .................')
#     itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])
# def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    return reply or defaultReply

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT, isGroupChat=True) # Group must be saved by current user/chat-bot
def text_reply(msg):
#     print('group  .................')
#     print('msg', msg)
#     print('msg[isAt]', msg['isAt'])
    if msg['isAt']:
#         print('group  .................@')
#         itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
        # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
        defaultReply = 'I received: ' + msg['Text']
        # 如果图灵Key出现问题，那么reply将会是None
        reply = get_response(msg['Text'])
        # a or b的意思是，如果a有内容，那么返回a，否则返回b
        # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
        # return reply or defaultReply
        if (reply != ''):
#             print(u'@%s\u2005%s' % (msg['ActualNickName'], reply))
            itchat.send(u'@%s\u2005%s' % (msg['ActualNickName'], reply), msg['FromUserName'])
        else:
#             print(u'@%s\u2005%s' % (msg['ActualNickName'], defaultReply))
            itchat.send(u'@%s\u2005%s' % (msg['ActualNickName'], defaultReply), msg['FromUserName'])


# In[ ]:

itchat.auto_login(True)
# itchat.auto_login()


# In[ ]:

itchat.run()


# In[ ]:

# itchat.logout()


# In[ ]:



