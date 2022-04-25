# -*- coding: utf-8 -*-
import vk_api
import time
import traceback
import random
from vk_api.longpoll import *
from vk_api.utils import *
from threading import Thread
from threading import Timer
import threading
import sqlite3
from apo_class import *
apo_host = Apostol_host('015ef2eaf71756ecdb2c1e82a03f9ddfb275cd2d7a1eb1c0805e1b8aa031b6497ac3a83e98d31178f0b52', 80)
misha = Apostol('29a65e147bb28e6ad0fa063cc77c802d04a7021f83b8a5824f9a5cf0a5c360e097ab8d1a8fd0471b46d29', 9)
sasha = Apostol('04342449943734a861844ead23182e99dce52c9c5952651f7a53f7917556e59dbadea2a9474a288673a96', 105)
andrey = Apostol('1f5abbe1f5feb9655fbb0a57d2afff66ebc4b6afd1bd09041d6a4976980f319e8c96507452b9394976c36', 34)
novichok = Apostol('352add914c4d32344762fe5881009fd89338d06783af329e71586f2bfc37c6d18465eb938a9623918c98b', 144)

def msg(vk_session, mess, event, chat, att= ''):
    vk_session.method('messages.send', {'chat_id': chat,
                                        'message': mess,
                                        'random_id': 0,
                                        'forward_message': time.sleep(0.000001),
                                        'reply_to': event.message_id,
                                        'attachment': att})


def main2():
    conn = sqlite3.connect('buffs.db')
    cur = conn.cursor()
    while True:
        try:
            for event in apo_host.listen():
                if event.from_chat and event.chat_id == apo_host.chat_id:#чат одного из апостолов, который хостом будет
                    msg_id = event.message_id
                    data = apo_host.getByMsgId(msg_id)
                    conv_id = data['conversation_message_id']
                    if '/проверка' in event.text.lower():
                        
                        prov = []
                        chat = misha.chat_id#чат Миши
                        try:
                            if misha.prov(misha.getByConvID(conv_id, 2000000000 + chat), 2000000000 + chat) == 1:
                                prov.append('Имя апо: навсегда-апостол-Михаил✅\nРасы: гоблин-гном; префикс - баф')
                            else:
                                prov.append('Имя апо: 🚫')
                        except Exception:
                            prov.append('Имя апо: 🚫')

                        chat = sasha.chat_id#чат Саши
                        try:
                            if sasha.prov(sasha.getByConvID(conv_id, 2000000000 + chat), 2000000000 + chat) == 1:
                                prov.append('Имя апо: Саша Смотритель✅\nРасы: человек-гном; префикс - 1баф')
                            else:
                                prov.append('Имя апо: 🚫')
                        except Exception:
                            prov.append('Имя апо: 🚫')

                        chat = novichok.chat_id  # чат новичка
                        try:
                            if novichok.prov(novichok.getByConvID(conv_id, 2000000000 + chat), 2000000000 + chat) == 1:
                                prov.append('Имя апо: просто апо✅\nРасы: человек-эльф; префикс - 2баф')
                            else:
                                prov.append('Имя апо: 🚫')
                        except Exception:
                            prov.append('Имя апо: 🚫')

                        chat = andrey.chat_id #чат Андрея
                        try:
                            if andrey.prov(andrey.getByConvID(conv_id, 2000000000 + chat), 2000000000 + chat) == 1:
                                prov.append('Имя воплы: добрая и очень большая вопла✅\n')
                            else:
                                prov.append('Имя апо: 🚫')

                        except Exception:
                            prov.append('Имя апо: 🚫')
                        mess = ''
                        print (prov)
                        for apo in prov:
                            mess = f'{mess}\n{apo}'
                        apo_host.buff('Результат проверки:', apo_host.chat_id, mess, msg_id)
                    if '/баф' in event.text.lower() and '/бафы' not in event.text.lower():
                        chat = misha.chat_id#чат Миши
                        str = event.text.lower()
                        buff = str.split("/баф")[1]
                        id = misha.getByConvID(conv_id, 2000000000 + chat)['id']
                        misha.buff('Благословение', chat, buff, id)
                    if '/1баф' in event.text.lower():
                        chat = sasha.chat_id#чат Саши
                        str = event.text.lower()
                        buff = str.split("/1баф")[1]
                        id = sasha.getByConvID(conv_id, 2000000000 + chat)['id']
                        sasha.buff('Благословение', chat, buff, id)
                    if '/2баф' in event.text.lower():
                        chat = novichok.chat_id#чат новичка
                        str = event.text.lower()
                        buff = str.split("/2баф")[1]
                        id = novichok.getByConvID(conv_id, 2000000000 + chat)['id']
                        novichok.buff('Благословение', chat, buff, id)
                    if '/свет' in event.text.lower():
                        chat = andrey.chat_id  # чат Андрея
                        id = andrey.getByConvID(conv_id, 2000000000 + chat)['id']
                        andrey.buff('', chat, 'очищение светом', id)
                    if '/очищение' in event.text.lower():
                        chat = andrey.chat_id  # чат Андрея
                        id = andrey.getByConvID(conv_id, 2000000000 + chat)['id']
                        andrey.buff('', chat, 'очищение', id)
        except Exception:
            itog = time.strftime("Month: %m, day:%d.\nTime: %H:%M:%S (+3 MSK, +5 EKB.)")
            err = traceback.format_exc()
            where = 'buff'
            go = 'The Error is find! . Date of Err: {}\n\n Where:\n\n{}\n\n Source: \n\n{}**********************************'.format(itog, err, where)
            
            print(go)

