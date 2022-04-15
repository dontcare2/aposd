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
apo_host = Apostol_host('46ef34eb58538b5590fd2a1a5a4a11ac5187c037dd28e494091c652ec827daf78cf63ef25c6286a98d613')
misha = Apostol('29a65e147bb28e6ad0fa063cc77c802d04a7021f83b8a5824f9a5cf0a5c360e097ab8d1a8fd0471b46d29')
sasha = Apostol('04342449943734a861844ead23182e99dce52c9c5952651f7a53f7917556e59dbadea2a9474a288673a96')
andrey = Apostol('1f5abbe1f5feb9655fbb0a57d2afff66ebc4b6afd1bd09041d6a4976980f319e8c96507452b9394976c36')
novichok = Apostol('043fb769174e60f4d742ff96eafbc56a7ebb59f6460a06fa5fbd21bac58620d5541df3fb35c5417a55fe8')

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
                if event.from_chat and event.chat_id == 80:#чат одного из апостолов, который хостом будет
                    msg_id = event.message_id
                    data = apo_host.getByMsgId(msg_id)
                    conv_id = data['conversation_message_id']
                    if '/проверка' in event.text.lower():
                        
                        prov = []
                        chat = 9#чат Миши
                        try:
                            if misha.prov(misha.getByConvID(conv_id, 2000000000 + chat), 2000000000 + chat) == 1:
                                prov.append('Имя апо: гладиапор✅\nРасы: гоблин-гном; префикс - баф')
                            else:
                                prov.append('Имя апо: 🚫')
                        except Exception:
                            prov.append('Имя апо: 🚫')

                        chat = 105#чат Саши
                        try:
                            if sasha.prov(sasha.getByConvID(conv_id, 2000000000 + chat), 2000000000 + chat) == 1:
                                prov.append('Имя апо: человек-резня✅\nРасы: человек-гном; префикс - 1баф')
                            else:
                                prov.append('Имя апо: 🚫')
                        except Exception:
                            prov.append('Имя апо: 🚫')

                        chat = 116  # чат новичка
                        try:
                            if novichok.prov(novichok.getByConvID(conv_id, 2000000000 + chat), 2000000000 + chat) == 1:
                                prov.append('Имя апо: просто апо✅\nРасы: человек-эльф; префикс - 2баф')
                            else:
                                prov.append('Имя апо: 🚫')
                        except Exception:
                            prov.append('Имя апо: 🚫')

                        chat = 34 #чат Андрея
                        try:
                            if andrey.prov(andrey.getByConvID(conv_id, 2000000000 + chat), 2000000000 + chat) == 1:
                                prov.append('Имя воплы: добрая вопла✅\n')
                            else:
                                prov.append('Имя апо: 🚫')

                        except Exception:
                            prov.append('Имя апо: 🚫')
                        mess = ''
                        print (prov)
                        for apo in prov:
                            mess = f'{mess}\n{apo}'
                        apo_host.buff('Результат проверки:', 80, mess, msg_id)
                    if '/баф' in event.text.lower() and '/бафы' not in event.text.lower():
                        chat = 9#чат Миши
                        str = event.text.lower()
                        buff = str.split("/баф")[1]
                        id = misha.getByConvID(conv_id, 2000000000 + chat)['id']
                        misha.buff('Благословение', chat, buff, id)
                    if '/1баф' in event.text.lower():
                        chat = 105#чат Саши
                        str = event.text.lower()
                        buff = str.split("/1баф")[1]
                        id = sasha.getByConvID(conv_id, 2000000000 + chat)['id']
                        sasha.buff('Благословение', chat, buff, id)
                    if '/2баф' in event.text.lower():
                        chat = 116#чат новичка
                        str = event.text.lower()
                        buff = str.split("/2баф")[1]
                        id = novichok.getByConvID(conv_id, 2000000000 + chat)['id']
                        novichok.buff('Благословение', chat, buff, id)
                    if '/свет' in event.text.lower():
                        chat = 34  # чат Андрея
                        id = andrey.getByConvID(conv_id, 2000000000 + chat)['id']
                        andrey.buff('', chat, 'очищение светом', id)
                    if '/очищение' in event.text.lower():
                        chat = 34  # чат Андрея
                        id = andrey.getByConvID(conv_id, 2000000000 + chat)['id']
                        andrey.buff('', chat, 'очищение', id)
        except Exception:
            itog = time.strftime("Month: %m, day:%d.\nTime: %H:%M:%S (+3 MSK, +5 EKB.)")
            err = traceback.format_exc()
            where = 'buff'
            go = 'The Error is find! . Date of Err: {}\n\n Where:\n\n{}\n\n Source: \n\n{}**********************************'.format(itog, err, where)
            
            print(go)

