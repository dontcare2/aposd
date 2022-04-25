# -*- coding: utf-8 -*-
import vk_api
import traceback
import math
import json
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import *
import time
from threading import Thread
from threading import Timer
import re
import sqlite3
from bs4 import BeautifulSoup
import apos_q
group_tok = '5d1cd3d8fa732ab7937cbdb3d5180d0503d762dfa4c9c9c958633579e213bbdec3a4dc98caa92718fc80e'

class BotLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('Bot Longpoll error', e)

bot_vk_session = vk_api.VkApi(token=group_tok)
Bot_longpoll = BotLongPoll(bot_vk_session, 212374607)               # Это лонгпулл группы
bot_vk = bot_vk_session.get_api()
print ("Bot ON!")
#отправка сообщений
def sender(id, text=None, keyboard=None, template=None, stiker=None):           # Отправка сообщений от группы
    bot_vk_session.method('messages.send', {
        'chat_id': id,
        'message': text,
        'random_id': 0,
        'keyboard': keyboard,
        'template': template,
        'sticker_id': stiker
    })
#конструктор обычной кнопки
def get_but(text, color):
    return {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"" + "1" + "\"}",
                    "label": f"{text}"
                },
                "color": f"{color}"
            }
#конструктор кнопки-ссылки
def get_link(text):
    return {
                "action": {
                    "type": "open_link",
                    "link": "https://vk.cc/9Efz1w",
                    "payload": "{\"button\": \"" + "1" + "\"}",
                    "label": f"{text}"
                }
    }    
#конструктор клавиатуры
def make_keyboard(k, c, o = True):
    keyboard = None
    if type(k) is list:
        if len(k) == 4:
            keyboard = {
                "inline": True,
                "buttons": [
                    [get_but(k[0], c[0]), get_but(k[1], c[1])],
                    [get_but(k[2], c[2]), get_but(k[3], c[3])]
                ],
                
            }
        elif len(k) == 5:
            keyboard = {
                "inline": True,
                "buttons": [
                    [get_but(k[0], c[0]), get_but(k[1], c[1])],
                    [get_but(k[2], c[2]),
                    get_but(k[3], c[3]), get_but(k[4], c[4])]
                ],
                
            }
        elif len(k) == 10:
            keyboard = {
                "inline": True,
                "buttons": [
                    [get_but(k[0], c[0]), get_but(k[1], c[1])],
                    [get_but(k[2], c[2]), get_but(k[3], c[3])],
                    [get_but(k[4], c[4]), get_but(k[5], c[5])],
                    [get_but(k[6], c[6]), get_but(k[7], c[7])],
                    [get_but(k[8], c[8]), get_but(k[9], c[9])]
                ],
                
            }
        elif len(k) == 9:
            keyboard = {
                "inline": True,
                "buttons": [
                    [get_but(k[0], c[0]), get_but(k[1], c[1])],
                    [get_but(k[2], c[2]), get_but(k[3], c[3])],
                    [get_but(k[4], c[4]), get_but(k[5], c[5])],
                    [get_but(k[6], c[6]), get_but(k[7], c[7])],
                    [get_but(k[8], c[8])]
                ],
                
            }
        elif len(k) == 8:
            keyboard = {
                "inline": True,
                "buttons": [
                    [get_but(k[0], c[0]), get_but(k[1], c[1])],
                    [get_but(k[2], c[2]), get_but(k[3], c[3])],
                    [get_but(k[4], c[4]), get_but(k[5], c[5])],
                    [get_but(k[6], c[6]), get_but(k[7], c[7])]
                ],
                
            }
        elif len(k) == 6:
            keyboard = {
                "inline": True,
                "buttons": [
                    [get_but(k[0], c[0]), get_but(k[1], c[1])],
                    [get_but(k[2], c[2]), get_but(k[3], c[3])],
                    [get_but(k[4], c[4]), get_but(k[5], c[5])],
                    
                ],
                
            }
        elif len(k) == 7:
            keyboard = {
                "inline": True,
                "buttons": [
                    [get_but(k[0], c[0]), get_but(k[1], c[1])],
                    [get_but(k[2], c[2]), get_but(k[3], c[3])],
                    [get_but(k[4], c[4]), get_but(k[5], c[5])],
                    [get_but(k[6], c[6])]
                ],
                
            }
        elif len(k) == 2:
            keyboard = {
                "inline": True,
                "buttons": [
                    [get_but(k[0], c[0]), get_but(k[1], c[1])]
                ],
                
            }
        elif len(k) == 3:
            keyboard = {
                "inline": True,
                "buttons": [
                    [get_but(k[0], c[0]), get_but(k[1], c[1])],
                    [get_but(k[2], c[2])]
                ],
                
            }
    else:
        keyboard = {
            "inline": True,
            "buttons": [
                [get_but(k, c)]
            ],
                
        }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard
def delete(ids, pid):
    bot_vk_session.method('messages.delete', {
                                                'cmids': ids + 1,
                                                'delete_for_all': 1,
                                                'peer_id': pid
                                            })
    bot_vk_session.method('messages.delete', {
                                                'cmids': ids,
                                                'delete_for_all': 1,
                                                'peer_id': pid
                                            })
def deleter(ids, pid):
    th = Timer(15.0, delete, args=(ids, pid))
    th.start()

def delone(ids, pid):
    bot_vk_session.method('messages.delete', {
                                                'cmids': ids,
                                                'delete_for_all': 1,
                                                'peer_id': pid
                                            })
def deleterone(ids, pid):
    th = Timer(15.0, delone, args=(ids, pid))
    th.start()
def getApo():
    conn = sqlite3.connect('buffs.db')
    cur = conn.cursor()
    cur.execute("SELECT last_buff FROM buffs WHERE apostol = ?;", (['buff']))
    buf = cur.fetchall()
    if len(buf) > 0:
        for b in buf:
            buff = b[0]
        current_time = time.time()
        if (current_time - float(buff)) > 305:
            c1 = 'positive'
        else:
            c1 = 'negative'
    else:
        c1 = 'primary'
    conn.commit()
    cur.execute("SELECT last_buff FROM buffs WHERE apostol = ?;", (['1buff']))
    buf = cur.fetchall()
    if len(buf) > 0:
        for b in buf:
            buff = b[0]
        current_time = time.time()
        if (current_time - float(buff)) > 305:
            c2 = 'positive'
        else:
            c2 = 'negative'
    else:
        c2 = 'primary'
    conn.commit()
    
    cur.execute("SELECT last_buff FROM buffs WHERE apostol = ?;", (['69buff']))
    buf = cur.fetchall()
    if len(buf) > 0:
        for b in buf:
            buff = b[0]
        current_time = time.time()
        if (current_time - float(buff)) > 305:
            c4 = 'positive'
        else:
            c4 = 'negative'
    else:
        c4 = 'primary'
    conn.commit()
    cur.execute("SELECT last_buff FROM buffs WHERE apostol = ?;", (['bbuff']))
    buf = cur.fetchall()
    if len(buf) > 0:
        for b in buf:
            buff = b[0]
        current_time = time.time()
        if (current_time - float(buff)) > 305:
            c5 = 'positive'
        else:
            c5 = 'negative'
    else:
        c5 = 'primary'
    conn.commit()
    cur.execute("SELECT last_buff FROM buffs WHERE apostol = ?;", (['+buff']))
    buf = cur.fetchall()
    if len(buf) > 0:
        for b in buf:
            buff = b[0]
        current_time = time.time()
        if (current_time - float(buff)) > 305:
            c6 = 'positive'
        else:
            c6 = 'negative'
    else:
        c6 = 'primary'
    conn.commit()
    cur.execute("SELECT last_buff FROM buffs WHERE apostol = ?;", (['777buff']))
    buf = cur.fetchall()
    if len(buf) > 0:
        for b in buf:
            buff = b[0]
        current_time = time.time()
        if (current_time - float(buff)) > 305:
            c7 = 'positive'
        else:
            c7 = 'negative'
    else:
        c7 = 'primary'
    conn.commit()

#sender(1, 'test!')
def main():
    group_tok = '5d1cd3d8fa732ab7937cbdb3d5180d0503d762dfa4c9c9c958633579e213bbdec3a4dc98caa92718fc80e'

    bot_vk_session = vk_api.VkApi(token=group_tok)
    Bot_longpoll = BotLongPoll(bot_vk_session, 212374607)               # Это лонгпулл группы
    bot_vk = bot_vk_session.get_api()
    for event in Bot_longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_chat:
                    msg = event.object.message['text']
                    lmsg = msg.lower()
                    cid = event.chat_id
                    pid = event.object.message['peer_id']
                    uid = event.from_user
                    timest = event.object.message['date']
                    #mid = event.message_id
                    cmid = event.object.message['conversation_message_id']
                    fwd = event.object.message['fwd_messages']
                    if '!кнопки2' in msg:  # если в замке завершена постройка, кнопки сбрасываются. Вызывать по новой вот этой командой.
                        k = 'Профиль'
                        c = 'secondary'
                        k1 = '🕍Замок'
                        c1 = 'secondary'
                        k2 = 'Хранилище'
                        c2 = 'primary'
                        k3 = '/бафы'
                        c3 = 'negative'
                        keyboard = {
                            "inline": False,
                            "buttons": [
                                [get_link(k), get_but(k1, c1)],
                                [get_but(k2, c2), get_but(k3, c3)]
                            ]
                        }
                        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
                        keyboard = str(keyboard.decode('utf-8'))
                        mid = sender(event.chat_id, '‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)

                    if '!кнопки' in msg:#если в замке завершена постройка, кнопки сбрасываются. Вызывать по новой вот этой командой.
                        k = 'Профиль'
                        c = 'secondary'
                        k1 = '🕍Замок'
                        c1 = 'secondary'
                        k2 = 'Хранилище'
                        c2 = 'primary'
                        k3 = '/бафы'
                        c3 = 'negative'
                        keyboard = {
                                        "inline": False,
                                        "buttons": [
                                            [get_link(k), get_but(k1, c1)],
                                            [get_but(k2, c2), get_but(k3, c3)]
                                        ]
                                    }
                        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
                        keyboard = str(keyboard.decode('utf-8'))
                        mid = sender(event.chat_id, '‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                    if '/бафы расы' in msg:
                        k=['/человека', '/эльфа', '/гнома', '/гоблина']#текст на кнопках
                        c=['positive', 'positive', 'primary', 'primary']#цвет кнопок
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Бафы рас:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/бафы статов' in msg:
                        k=['/атаки', '/защиты', '/удачи']
                        c=['negative', 'primary', 'positive']
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Бафы статов:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/бафы' in msg and 'статов' not in msg and 'расы' not in msg:
                        k=['/бафы расы', '/бафы статов', '/многобаф']
                        c=['primary', 'secondary', 'secondary']
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Меню бафов:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/черны' in msg:
                        k=['/прок неудачи', '/прок добычи', '/прок боли']
                        c=['primary', 'secondary', 'negative']
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Наши чернокнижники:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/паладины' in msg:
                        k=['/солнце', '/дождик', '/очисти']
                        c=['primary', 'secondary', 'primary']
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Наши палладины:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/человека' in msg:
                        c1 = 'positive'
                        c2 = 'positive'
                        #c3 = 'positive'
                            
                        k=['/1баф человека','/2баф человека']
                        c=[c1, c2]
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Воть:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/эльфа' in msg:
                        c1 = 'positive'
                        k='/2баф эльфа'
                        c=c1
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Воть:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/гнома' in msg:
                        c1 = 'positive'
                        c2 = 'positive'
                        k=['/баф гнома', '/1баф гнома']
                        c=[c1, c2]
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Воть:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/гоблина' in msg:
                        c1 = 'positive'
                        k = '/баф гоблина'
                        c = c1
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Воть:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/нежебаф' in msg:
                        pass
                    if '/оркобаф' in msg:
                        pass
                    if '/демонобаф' in msg:
                        pass
                    if '/атаки' in msg:
                        c1 = 'positive'
                        c2 = 'positive'
                        c3 = 'positive'
                        k = ['/баф атаки', '/1баф атаки', '/2баф атаки']
                        c = [c1, c2, c3]
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Воть:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/защиты' in msg:
                        c1 = 'positive'
                        c2 = 'positive'
                        c3 = 'positive'
                        k = ['/баф защиты', '/1баф защиты', '/2баф защиты']
                        c = [c1, c2, c3]
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Воть:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/удачи' in msg:
                        c1 = 'positive'
                        c2 = 'positive'
                        c3 = 'positive'
                        k = ['/баф удачи', '/1баф удачи', '/2баф удачи']
                        c = [c1, c2, c3]
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Воть:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/многобаф' in msg:
                        k = ['/баф атаки', '/1баф защиты', '/2баф удачи', '/1баф человека']
                        c = ['positive', 'negative', 'positive', 'negative']
                        keyboard = make_keyboard(k, c)
                        mid = sender(event.chat_id, 'Ну-кась:‍‍    ‌‌‍‍   ‍‍    ‌‌‍‍   ', keyboard)
                        deleter(cmid, pid)
                    if '/баф' in msg or '/1баф' in msg in msg or '/2баф' in msg or '/777баф' in msg or '/ббаф' in msg or '+баф' in msg or '/прок' in msg or '/свет' in msg or '/очищение' in msg:
                        deleterone(cmid, pid)
                    if 'благословение' in msg.lower() or'проклятие'in msg.lower() or'очищение'in msg.lower() or 'осмотреть' in msg.lower():
                        deleterone(cmid, pid)
        except:
            itog = time.strftime("Месяц: %m, день месяца:%d.\nВремя ошибки: %H:%M:%S (+3 по МСК, +5 по ЕКБ.)")
            err = traceback.format_exc()
            print('Найдена ошибка! Веду отчет. Дата отчета: {}\n\nГде ошибка:\n\n{}'.format(itog, err))


th1 = Thread(target=main, daemon=True)
th1.start()
th2 = Thread(target=apos_q.main2, daemon=True)
th2.start()
th1.join()
th2.join()