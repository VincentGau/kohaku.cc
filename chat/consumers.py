#!/usr/bin/env python
# -*- coding: utf-8 -*-

from channels import Group

online_user = []


# Connected to websocket.connect
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("chat").add(message.reply_channel)

    print "new user"


# Connected to websocket.receive
def ws_message(message):
    flag, username, content = message.content["text"].split("&")
    if flag == '0':
        # user join
        online_user.append(username)

    elif flag == '1':
        # user leaves
        online_user.remove(username)

    users = '#'.join(online_user)

    # // socket 消息格式 flag&username&content
    # // flag 取值为 0|1|2， 0表示新用户加入，1表示用户离开，2表示用户发送消息
    # // 如果flag 取值为 0或1，content内容为在线用户列表，如果flag 取值为2， content为发送的消息内容
    content_sent = message.content["text"] if flag == '2' else '&'.join([flag, username, users])

    # print online_user
    # print message.content['text']

    Group("chat").send({
        "text": content_sent,
    })


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)
    print "user leaves"
