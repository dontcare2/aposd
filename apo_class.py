# -*- coding: utf-8 -*-
from ast import Try
import vk_api
from vk_api.longpoll import *
from vk_api.utils import *
import sqlite3
class Apostol_host(object):
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.vk_session = vk_api.VkApi (token=token)
        self.longpoll = VkLongPoll (self.vk_session)
        self.vk = self.vk_session.get_api ()
        self.conn = sqlite3.connect('buffs.db')
        self.cur = self.conn.cursor()
    def getByConvID(self, conv, peer):
        result = self.vk_session.method('messages.getByConversationMessageId', {'peer_id': peer,
                                            'conversation_message_ids': conv,
                                            'access_token': self.token
                                            })
        return result['items'][0]
    def getByMsgId(self, id):
        result = self.vk_session.method('messages.getById', {'message_ids': id,
                                        'access_token': self.token
                                        })
        return result['items'][0]
    def listen(self):
        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.text.lower():
                        yield event
            except Exception:
                pass
    def to_query(self, ):
        pass
        '''self.cur.execute("INSERT INTO que VALUES(?, ?)", data)
        self.conn.commit()'''
    def buff(self, pref, chat, buff, msg_id, att = None):
        result = self.vk_session.method('messages.send', {'chat_id': chat,
                                        'message': '{} {}'.format(pref, buff),
                                        'random_id': 0,
                                        'reply_to': msg_id,
                                        'attachment': att})

class Apostol(object):
    def __init__(self, token, chat_id):
        try:
            self.token = token
            self.chat_id = chat_id
            self.vk_session = vk_api.VkApi (token=token)
            self.longpoll = VkLongPoll (self.vk_session)
            self.vk = self.vk_session.get_api ()
        except Exception:
            print ('Invalid token detected!')
        
    def getByConvID(self, conv, peer):
        result = self.vk_session.method('messages.getByConversationMessageId', {'peer_id': peer,
                                            'conversation_message_ids': conv,
                                            'access_token': self.token
                                            })
        return result['items'][0]
    def getByMsgId(self, id):
        result = self.vk_session.method('messages.getById', {'message_ids': id,
                                        'access_token': self.token
                                        })
        return result['items'][0]
    def buff(self, pref, chat, buff, msg_id, att = None):
        result = self.vk_session.method('messages.send', {'chat_id': chat,
                                        'message': '{} {}'.format(pref, buff),
                                        'random_id': 0,
                                        'reply_to': msg_id,
                                        'attachment': att})
        return result
    def prov(self, id, peer):
        result = self.vk_session.method('messages.setActivity', {'type': 'typing',
                                        'peer_id': peer,
                                        'access_token': self.token
                                        })
        return result