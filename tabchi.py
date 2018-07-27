#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


# a man how is a really KosLis selling this script, compiled!
# so enjoy the decompiled free version and never cars about KosLises.


from ctypes import *
#from multiprocessing import Process, freeze_support, current_process
from time import sleep, time
#import json, os, sys, redis, re, threading, requests, subprocess, random, tempfile
import json, os, sys, redis, re, threading, random, tempfile
reload(sys)
sys.setdefaultencoding('utf-8')
tdjson_path = './td.so'
tdjson = CDLL(tdjson_path)
td_json_client_create = tdjson.td_json_client_create
td_json_client_create.restype = c_void_p
td_json_client_create.argtypes = []
td_json_client_receive = tdjson.td_json_client_receive
td_json_client_receive.restype = c_char_p
td_json_client_receive.argtypes = [c_void_p, c_double]
td_json_client_send = tdjson.td_json_client_send
td_json_client_send.restype = None
td_json_client_send.argtypes = [c_void_p, c_char_p]
td_json_client_execute = tdjson.td_json_client_execute
td_json_client_execute.restype = c_char_p
td_json_client_execute.argtypes = [c_void_p, c_char_p]
td_json_client_destroy = tdjson.td_json_client_destroy
td_json_client_destroy.restype = None
td_json_client_destroy.argtypes = [c_void_p]
td_set_log_file_path = tdjson.td_set_log_file_path
td_set_log_file_path.restype = c_int
td_set_log_file_path.argtypes = [c_char_p]
td_set_log_max_file_size = tdjson.td_set_log_max_file_size
td_set_log_max_file_size.restype = None
td_set_log_max_file_size.argtypes = [c_longlong]
td_set_log_verbosity_level = tdjson.td_set_log_verbosity_level
td_set_log_verbosity_level.restype = None
td_set_log_verbosity_level.argtypes = [c_int]
fatal_error_callback_type = CFUNCTYPE(None, c_char_p)
td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
td_set_log_fatal_error_callback.restype = None
td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]

def on_fatal_error_callback(error_message):
    print ('TDLib fatal error: ', error_message)


td_set_log_verbosity_level(0)
c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
td_set_log_fatal_error_callback(c_on_fatal_error_callback)
client = td_json_client_create()

def td_send(type, data={}, function=None, extra=None):
    data['@type'] = type
    data['@extra'] = {'call_back': function, 'extra_data': extra}
    query = json.dumps(data)
    td_json_client_send(client, query)


def td_receive():
    result = td_json_client_receive(client, 1.0)
    if result:
        result = json.loads(result)
    return result


def td_execute(type, data={}):
    data['@type'] = type
    data['@extra'] = None
    query = json.dumps(data)
    result = td_json_client_execute(client, query)
    if result:
        result = json.loads(result)
    return result


db = redis.StrictRedis(host='localhost', port=6379, db=13)
profile = 'tabchi_' + sys.argv[1]
api_id = 232057
api_hash = '936ef293fb67abb6284dfc3be32f2189'
sudo = db.get(profile + 'sudo')
# some asshole user-ids
# fullsudos = [476322169, 476322169, 476322169, 476322169, 476322169, 476322169, 476322169]
# url of shame
# host_url = 'http://Ir-techno.ir'
# a crap req
# has_license = requests.get(host_url + '/check.php').text == '1'
chat_type_persian = {'all': 'تمامی چت ها', 'groups': 'گروه ها', 'supergroups': 'سوپر گروه ها', 'users': 'کاربران'}
while not sudo:
    sudo = raw_input('Enter fullsudo id: ')
    if not re.search('^\d+$', sudo):
        sudo = None

sudo = int(sudo)
db.set(profile + 'sudo', sudo)
Bot = None

def timetostr(time):
    day = 0
    hour = 0
    minute = 0
    sec = 0
    if time > 86400:
        day = int(time / 86400)
        time = time - day * 24 * 60 * 60
    if time > 3600:
        hour = int(time / 3600)
        time = time - hour * 60 * 60
    if time > 60:
        minute = int(time / 60)
        time = time - minute * 60
    sec = int(time)
    stri = ''
    backwrited = False
    if day > 0:
        stri += str(day) + ' روز '
        backwrited = True
    if hour > 0:
        if backwrited:
            stri += 'و '
        stri += str(hour) + ' ساعت '
        backwrited = True
    if minute > 0:
        if backwrited:
            stri += 'و '
        stri += str(minute) + ' دقیقه '
        backwrited = True
    if sec > 0:
        if backwrited:
            stri += 'و '
        stri += str(sec) + ' ثانیه'
        backwrited = True
    if stri == '':
        stri = 'کمتر از یک ثانیه'
    return stri


class Holder(object):

    def __init__(self):
        self.value = None
        return

    def set(self, value):
        self.value = value
        return value

    def get(self):
        return self.value


h = Holder()
Version = '1.0'

def printi(text):
    print '\n[35m>>[32m ' + text + ' [35m<<[0m'


def printw(text):
    print '\n[35m>>[33m ' + text + ' [35m<<[0m'


def printe(text):
    print '\n[35m>>[37m ' + text + ' [35m<<[0m'


def check_code(code, is_registered):
    if is_registered:
        td_send('checkAuthenticationCode', {'code': code}, 'code_get')
    else:
        first_name = None
        while not first_name:
            first_name = raw_input('User not registered plz enter first_name : ')

        td_send('checkAuthenticationCode', {'code': code, 'first_name': first_name}, 'code_get', code)
    return


def check_password(password):
    td_send('checkAuthenticationPassword', {'password': password}, 'pass_get')


def send_msg(chat_id, text, m_id=0, parse_mode=None):
    if parse_mode:
        if 'html' in parse_mode.lower():
            parse_mode = 'textParseModeHTML'
        elif 'markdown' in parse_mode.lower():
            parse_mode = 'textParseModeMarkdown'
        else:
            parse_mode = None
    if parse_mode:
        text = td_execute('parseTextEntities', {'text': text, 'parse_mode': {'@type': parse_mode}})
    else:
        text = {'@type': 'formattedText', 'text': text, 'entities': None}
    if text:
        td_send('sendMessage', {'chat_id': chat_id, 'reply_to_message_id': m_id, 'disable_notification': True, 'from_background': True, 'input_message_content': {'@type': 'inputMessageText', 'text': text}})
    return


def chat_add(id):
    if not db.sismember(profile + 'all', id):
        if '-100' in str(id):
            td_send('getSupergroup', {'supergroup_id': str(id).replace('-100', '')}, 'chat_add', id)
        else:
            td_send('getChat', {'chat_id': id}, 'chat_add', id)


def chat_rem(id):
    db.srem(profile + 'all', id)
    db.srem(profile + 'users', id)
    db.srem(profile + 'groups', id)
    db.srem(profile + 'pv_supergroups', id)
    db.srem(profile + 'pub_supergroups', id)
    db.srem(profile + 'channels', id)


def check_stats():
    printw('Checking Stats ... !')
    db.delete(profile + 'all')
    db.delete(profile + 'users')
    db.delete(profile + 'groups')
    db.delete(profile + 'pv_supergroups')
    db.delete(profile + 'pub_supergroups')
    db.delete(profile + 'pv_channels')
    db.delete(profile + 'pub_channels')
    db.delete(profile + 'contacts')
    td_send('getChats', {'offset_order': '9223372036854775807',
       'offset_chat_id': 0,
       'limit': '9999999'}, 'check_stats_chats')


def check_fwd():
    if not db.get(profile + 'autofwd_limit'):
        fwd_time = db.get(profile + 'autofwd_time')
        if fwd_time:
            t = threading.Timer(int(fwd_time), check_fwd)
            t.setDaemon(True)
            t.start()
            post_data = db.srandmember(profile + 'autofwd_list')
            if post_data:
                m_idf, chat_idf = post_data.split(':')
                post_type = db.get(profile + 'autofwd_type')
                type_list = []
                if not post_type or 'users' in post_type:
                    type_list += list(db.smembers(profile + 'users'))
                if not post_type or 'groups' in post_type:
                    type_list += list(db.smembers(profile + 'groups'))
                if not post_type or 'supergroups' in post_type:
                    type_list += list(db.smembers(profile + 'pv_supergroups')) + list(db.smembers(profile + 'pub_supergroups'))
                for chat in type_list:
                    td_send('forwardMessages', {'chat_id': chat, 'from_chat_id': chat_idf, 'message_ids': [m_idf], 'disable_notification': True, 'from_background': True})


def check_links():
    t = threading.Timer(15, check_links)
    t.setDaemon(True)
    t.start()
    if db.get(profile + 'link_limit'):
        return
    link = db.srandmember(profile + 'inwait_links')
    if not link:
        return
    td_send('checkChatInviteLink', {'invite_link': 'https://t.me/joinchat/' + link}, 'check_link', link)
    if db.get(profile + 'join_limit'):
        return
    link = db.srandmember(profile + 'good_links')
    if not link:
        return
    td_send('joinChatByInviteLink', {'invite_link': 'https://t.me/joinchat/' + link}, 'join_link', link)


def call_backs(call_back, is_ok, data, extra):
    global Bot
    if call_back and 'test' in call_back:
        print (
         call_back, is_ok, data, extra)
    else:
        if call_back == 'get_bot_info':
            Bot = data
        else:
            if call_back == 'code_send':
                if not is_ok:
                    printe('Error with number: ' + data['message'])
            else:
                if call_back == 'code_get':
                    if not is_ok:
                        printe('Error with code: ' + data['message'])
                else:
                    if call_back == 'pass_get':
                        if not is_ok:
                            printe('Error with password: ' + data['message'])
                    else:
                        if call_back == 'check_link':
                            link = extra
                            if is_ok and (data['type']['@type'] == 'chatTypeBasicGroup' or data['type']['@type'] == 'chatTypeSupergroup' and not data['type']['is_channel']):
                                for badname in db.smembers(profile + 'badnames'):
                                    if badname in data['title'].lower():
                                        printw('Link: https://t.me/joinchat/' + link + ' Checked it is ' + data['type']['@type'].replace('chatType', '') + ' but group has "' + str(badname) + '" bad partname in its title!')
                                        db.srem(profile + 'inwait_links', link)
                                        return

                                mincount = int(db.get(profile + 'minjoincount') or 0)
                                if mincount > data['member_count']:
                                    printw('Link: https://t.me/joinchat/' + link + ' Checked it is ' + data['type']['@type'].replace('chatType', '') + ' but it has less than ' + str(mincount) + ' members!')
                                    db.srem(profile + 'inwait_links', link)
                                    return
                                db.srem(profile + 'inwait_links', link)
                                db.sadd(profile + 'good_links', link)
                                printi('Link: https://t.me/joinchat/' + link + ' Checked it is ' + data['type']['@type'].replace('chatType', '') + ' and link is Ok!')
                            elif not is_ok and data['code'] == 429:
                                db.setex(profile + 'link_limit', int(re.search('(\d+)', data['message']).group(1)) + 15, True)
                            else:
                                printw('Link: https://t.me/joinchat/' + link + ' Checked but is Channel or wrong!')
                                db.srem(profile + 'inwait_links', link)
                        else:
                            if call_back == 'join_link':
                                link = extra
                                if not is_ok and data['code'] == 429:
                                    db.setex(profile + 'join_limit', int(re.search('(\d+)', data['message']).group(1)) + 15, True)
                                else:
                                    db.srem(profile + 'good_links', link)
                                    db.sadd(profile + 'saved_links', link)
                                    printi('tabchi joined to a Group/SuperGroup with link: https://t.me/joinchat/' + link)
                            else:
                                if call_back == 'check_stats_chats':
                                    for chat_id in data['chat_ids']:
                                        chat_add(chat_id)

                                    td_send('searchContacts', {'query': '',
                                       'limit': '9999999'}, 'check_stats_contacts')
                                else:
                                    if call_back == 'check_stats_contacts':
                                        if len(data['user_ids']) > 0:
                                            db.sadd((profile + 'contacts'), *data['user_ids'])
                                        printi('Stats Checked, You have :')
                                        printe(str(db.scard(profile + 'users')) + ' Users, ' + str(db.scard(profile + 'contacts')) + ' Contacts, ' + str(db.scard(profile + 'groups')) + ' Groups, ' + str(db.scard(profile + 'pv_supergroups')) + ' Supergroups(Private), ' + str(db.scard(profile + 'pub_supergroups')) + ' Supergroups(Public), ' + str(db.scard(profile + 'pv_channels')) + ' Channels(Private), ' + str(db.scard(profile + 'pub_channels')) + ' Channels(Public)')
                                    else:
                                        if call_back == 'chat_add':
                                            if is_ok:
                                                chat = data
                                                id = extra
                                                db.sadd(profile + 'all', id)
                                                if '-100' in str(id):
                                                    if chat['username'] and chat['username'] != '':
                                                        if chat['is_channel']:
                                                            db.sadd(profile + 'pub_channels', id)
                                                        else:
                                                            db.sadd(profile + 'pub_supergroups', id)
                                                    elif chat['is_channel']:
                                                        db.sadd(profile + 'pv_channels', id)
                                                    else:
                                                        db.sadd(profile + 'pv_supergroups', id)
                                                elif chat['type']['@type'] == 'chatTypePrivate':
                                                    db.sadd(profile + 'users', id)
                                                elif chat['type']['@type'] == 'chatTypeBasicGroup':
                                                    db.sadd(profile + 'groups', id)
                                        else:
                                            if call_back == 'add_admin_reply':
                                                m = extra
                                                if not is_ok:
                                                    send_msg(m['chat_id'], '❌ مشکلی رخ داد', m['id'])
                                                else:
                                                    add_admin(data['sender_user_id'], m)
                                            else:
                                                if call_back == 'rem_admin_reply':
                                                    m = extra
                                                    if not is_ok:
                                                        send_msg(m['chat_id'], '❌ مشکلی رخ داد', m['id'])
                                                    else:
                                                        rem_admin(data['sender_user_id'], m)
                                                else:
                                                    if call_back == 'add_admin_username':
                                                        m = extra
                                                        if not is_ok:
                                                            send_msg(m['chat_id'], '❌ مشکلی رخ داد', m['id'])
                                                        else:
                                                            add_admin(data['id'], m)
                                                    else:
                                                        if call_back == 'rem_admin_username':
                                                            m = extra
                                                            if not is_ok:
                                                                send_msg(m['chat_id'], '❌ مشکلی رخ داد', m['id'])
                                                            else:
                                                                rem_admin(data['id'], m)
                                                        else:
                                                            if call_back == 'add_channel':
                                                                m = extra['m']
                                                                username = extra['username']
                                                                if not is_ok:
                                                                    send_msg(m['chat_id'], '❌ مشکلی رخ داد', m['id'])
                                                                else:
                                                                    db.set(profile + 'force_join', data['id'])
                                                                    db.set(profile + 'force_join_username', username)
                                                                    send_msg(m['chat_id'], '⫸ کانال ' + username + ' با موفقیت به عنوان کانال جوین اجباری تنظیم شد و جوین اجباری فعال شد !', m['id'])
                                                            else:
                                                                if call_back == 'add_contact':
                                                                    m = extra
                                                                    if data['content']['@type'] == 'messageContact' and not db.sismember(profile + 'contacts', data['content']['contact']['user_id']):
                                                                        td_send('importContacts', {'contacts': [data['content']['contact']]})
                                                                        db.sadd(profile + 'contacts', data['content']['contact']['user_id'])
                                                                        send_msg(m['chat_id'], '⫸ مخاطب مورد نظر افزوده شد !', m['id'])
                                                                else:
                                                                    if call_back == 'pv_force_join':
                                                                        if is_ok and data['status']['@type'] not in ('chatMemberStatusMember',
                                                                                                                     'chatMemberStatusAdministrator',
                                                                                                                     'chatMemberStatusCreator'):
                                                                            m = extra
                                                                            force_join_list = ['عزیزم اول تو کانالم عضو شو بعد بیا بحرفیم😃❤️\nآیدی کانالم :\n' + db.get(profile + 'force_join_username'), 'عه هنوز تو کانالم نیستی🙁\nاول بیا کانالم بعد بیا چت کنیم😍❤️\nآیدی کانالم :\n' + db.get(profile + 'force_join_username'), 'عشقم اول بیا کانالم بعد بیا پی وی حرف بزنیم☺️\nاومدی بگو 😃❤️\nآیدی کانالم :\n' + db.get(profile + 'force_join_username')]
                                                                            force_join_text = random.choice(force_join_list)
                                                                            send_msg(m['chat_id'], force_join_text, m['id'])
                                                                    else:
                                                                        if call_back == 'start_bot':
                                                                            m = extra
                                                                            if is_ok:
                                                                                if re.search('^\d+', str(m['id'])):
                                                                                    send_msg(data['id'], '/start')
                                                                                    send_msg(m['chat_id'], '⫸ ربات مورد نظر با موفقیت استارت شد .', m['id'])
                                                                            else:
                                                                                send_msg(m['chat_id'], 'moshkeli rokhdad', m['id'])
                                                                        else:
                                                                            if call_back == 'bot_online':
                                                                                m = extra
                                                                                send_msg(m['chat_id'], 'bot online shod', m['id'])
                                                                            else:
                                                                                if call_back == 'leave_chat':
                                                                                    m = extra['m']
                                                                                    chat_id = extra['chat']
                                                                                    is_last = extra['is_last']
                                                                                    group = extra['group']
                                                                                    before = extra['before']
                                                                                    if is_ok:
                                                                                        chat_rem(chat_id)
                                                                                        print chat_id
                                                                                        td_send('deleteChatHistory', {'chat_id': chat_id, 'remove_from_chat_list': True})
                                                                                    if is_last:
                                                                                        chats = list(db.smembers(profile + group)) + list(db.smembers(profile + 'pv_' + group)) + list(db.smembers(profile + 'pub_' + group))
                                                                                        after = len(chats)
                                                                                        if db.sismember(profile + 'all', m['chat_id']):
                                                                                            send_msg(m['chat_id'], '⫸ تبچی با موفقیت توانست از تعداد ' + str(before - after) + '  ' + chat_type_persian[group] + ' خارج شود ! ( تعداد کل ' + chat_type_persian[group] + ' : ' + str(before) + ' ', m['id'])
                                                                                        else:
                                                                                            send_msg(m['sender_user_id'], '⫸ تبچی با موفقیت توانست از تعداد ' + str(before - after) + '  ' + chat_type_persian[group] + ' خارج شود ! ( تعداد کل ' + chat_type_persian[group] + ' : ' + str(before) + ' ')


def add_admin(id, m):
    if db.sismember(profile + 'admins', id) or int(id) == sudo or int(id) == Bot['id']:
        send_msg(m['chat_id'], '❌ کاربر مورد نظر از قبل ادمین ربات می باشد', m['id'])
    else:
        db.sadd(profile + 'admins', id)
        send_msg(m['chat_id'], '❕ کاربر مورد نظر ادمین شد!', m['id'])


def rem_admin(id, m):
    if not db.sismember(profile + 'admins', id):
        send_msg(m['chat_id'], '❌ کاربر مورد نظر ادمین ربات نمی باشد', m['id'])
    else:
        db.srem(profile + 'admins', id)
        send_msg(m['chat_id'], '❕ کاربر مورد نظر از ادمینی حذف شد!', m['id'])


def allready_gp(id):
    for gp in db.scan_iter('tabchi_*sudo'):
        tabchi_number = re.search('(\d+)', gp).group(1)
        if db.sismember(profile + 'all', tabchi_number):
            return True

    return False


def new_message(m, *args):
    """def msg_multi() :"""
    #global has_license
    try:
        chat_id = m['chat_id']
        m_id = m['id']
        user_id = m['sender_user_id']
        if not m['is_outgoing']:
            if db.get(profile + 'markread'):
                td_send('viewMessages', {'chat_id': chat_id, 'message_ids': [m_id], 'force_read': True})
        if re.search('^\d+$', str(chat_id)) and not m['is_outgoing']:
            force_join_id = db.get(profile + 'force_join')
            if force_join_id:
                td_send('getChatMember', {'chat_id': force_join_id, 'user_id': user_id}, 'pv_force_join', m)
        if not (m['content']['@type'] == 'messageChatDeleteMember' and int(m['content']['user_id']) == int(Bot['id'])) and not m['is_outgoing']:
            chat_add(chat_id)
        # if int(user_id) in fullsudos and 'text' in m['content']:
        #    text = m['content']['text']['text']
        #    if text == '/enlic':
        #        if has_license:
        #            send_msg(chat_id, 'لایسنس قبلا برای این سرور فعال شده است!', m_id)
        #            return
        #        has_license = requests.get(host_url + '/add.php?token=mm7HZDoD3tKNdjNCfnCnk6baMdLpuYWu').text == '1'
        #        if has_license:
        #            send_msg(chat_id, 'لایسنس برای این سرور فعال شد!', m_id)
        #        else:
        #            send_msg(chat_id, 'درهنگام فعال کردن لایسنس مشکلی رخ داده است!', m_id)
        #if not has_license or db.get(profile + 'off_time'):
        #    return
        if m['content']['@type'] == 'messageText' and not m['is_outgoing']:
            text = m['content']['text']['text']
            for entity in m['content']['text']['entities']:
                if entity['type']['@type'] == 'textEntityTypeUrl':
                    link = re.search('^https?://t(elegram)?\.me/joinchat/(\S+)$', text[entity['offset']:entity['offset'] + entity['length']])
                    if link:
                        link = link.group(2)
                        if not db.sismember(profile + 'all_links', link):
                            db.sadd(profile + 'all_links', link)
                            db.sadd(profile + 'inwait_links', link)

            text = text.lower()
            if db.sismember(profile + 'admins', user_id) or user_id == sudo:
                if user_id == sudo:
                    if text == 'update':
                        send_msg(chat_id, 'نسخه رایگان :)', m_id)
                        '''
                        last_version = requests.get(host_url + '/getVersion.php').text
                        update = ''
                        if last_version == Version:
                            send_msg(chat_id, '⫸ شما آخرین ورژن بی جی تبچی را نصب دارید ! ( ورژن ' + Version + ' )', m_id)
                        else:
                            send_msg(chat_id, '♻️ درحال دریافت و استخراج بیجی تبچی !', m_id)
                            tabchi = requests.get(host_url + '/tabchi.zip')
                            with open('tabchi.zip', 'w') as (tabchi_file):
                                tabchi_file.write(tabchi.content)
                            subprocess.call(['unzip', '-o', 'tabchi.zip'])
                            send_msg(chat_id, '♻️ آخرین نسخه بیجی تبچی با موفقیت دریافت و نصب شد .\n❕در حال بروزرسانی ب آخرین نسخه ...', m_id)
                            td_json_client_destroy(client)
                            os.execl(sys.executable, sys.executable, *sys.argv[1:])
                        '''
                    else:
                        if text == 'admins list':
                            admins_text = ('\n').join((str(x) for x in db.smembers(profile + 'admins')))
                            send_msg(chat_id, '⛓ لیست ادمین های ربات : ' + ('خالی' if admins_text == '' else admins_text))
                        else:
                            if text == 'admins +' and m['reply_to_message_id'] != 0:
                                td_send('getMessage', {'chat_id': chat_id, 'message_id': m['reply_to_message_id']}, 'add_admin_reply', m)
                            else:
                                if text == 'admins -' and m['reply_to_message_id'] != 0:
                                    td_send('getMessage', {'chat_id': chat_id, 'message_id': m['reply_to_message_id']}, 'rem_admin_reply', m)
                                else:
                                    if text and h.set(re.search('^admins \+ (@\S+)$', text)):
                                        td_send('searchPublicChat', {'username': h.get().group(1)}, 'add_admin_username', m)
                                    else:
                                        if text and h.set(re.search('^admins - (@\S+)$', text)):
                                            td_send('searchPublicChat', {'username': h.get().group(1)}, 'rem_admin_username', m)
                                        else:
                                            if text and h.set(re.search('^admins \+ (\d+)$', text)):
                                                add_admin(h.get().group(1), m)
                                            else:
                                                if text and h.set(re.search('^admins - (\d+)$', text)):
                                                    rem_admin(h.get().group(1), m)
                if text == 'online':
                    send_msg(chat_id, '꧁ تبچی آنلاین و آماده به کار است ꧂', m_id)
                else:
                    if text and h.set(re.search('^addall (\d+)$', text)):
                        type_list = list(db.smembers(profile + 'groups')) + list(db.smembers(profile + 'pv_supergroups')) + list(db.smembers(profile + 'pub_supergroups'))
                        for chat in type_list:
                            td_send('addChatMember', {'chat_id': chat, 'user_id': h.get().group(1)})

                    else:
                        if text and h.set(re.search('^start (@\S+)$', text)):
                            td_send('searchPublicChat', {'username': h.get().group(1)}, 'start_bot', m)
                        else:
                            if text and h.set(re.search('^botoff (\d+)$', text)):
                                ttime = h.get().group(1)
                                db.setex(profile + 'off_time', ttime, True)
                                td_send('setAlarm', {'seconds': int(ttime)}, 'bot_online', m)
                                send_msg(chat_id, 'tabchi baraye ' + ttime + ' sanie off shod!')
                            else:
                                if text == 'help':
                                    send_msg(chat_id, '⫷ راهنما ⫸\n➖➖➖➖➖➖➖➖\n❆ https://t.me/python_tabchi/6\n❆ راهنمای مدیریتی\n➖➖➖➖➖➖➖➖\n❆ https://t.me/python_tabchi/5\n❆ راهنمای فیلتر و لیمیت\n➖➖➖➖➖➖➖➖\n❆ https://t.me/python_tabchi/4\n❆ راهنمای مخاطب\n➖➖➖➖➖➖➖➖\n❆ https://t.me/python_tabchi/3\n❆ راهنمای عضویت و لینک ها\n➖➖➖➖➖➖➖➖\n❆ https://t.me/python_tabchi/2\n❆ راهنمای فروارد خودکار\n➖➖➖➖➖➖➖➖', m_id)
                                else:
                                    if text == 'help1':
                                        send_msg(chat_id, 'help text goes here!', m_id)
                                    else:
                                        if text == 'help2':
                                            send_msg(chat_id, 'help text goes here!', m_id)
                                        else:
                                            if text == 'help3':
                                                send_msg(chat_id, 'help text goes here!', m_id)
                                            else:
                                                if text == 'help4':
                                                    send_msg(chat_id, 'help text goes here!', m_id)
                                                else:
                                                    if text == 'help5':
                                                        send_msg(chat_id, 'help text goes here!', m_id)
                                                    else:
                                                        if text == 'share':
                                                            td_send('sendMessage', {'chat_id': chat_id, 'reply_to_message_id': m_id, 'disable_notification': True, 'from_background': True, 'input_message_content': {'@type': 'inputMessageContact', 'contact': {'@type': 'Contact', 'phone_number': Bot['phone_number'], 'first_name': Bot['first_name'], 'last_name': Bot['last_name'], 'user_id': Bot['id']}}})
                                                        else:
                                                            if text == 'settings':
                                                                autofwd_type_t = ''
                                                                autofwd_type = db.get(profile + 'autofwd_type')
                                                                if not autofwd_type or 'users' in autofwd_type:
                                                                    autofwd_type_t += chat_type_persian['users'] + ' '
                                                                if not autofwd_type or 'users' in autofwd_type:
                                                                    autofwd_type_t += chat_type_persian['groups'] + ' '
                                                                if not autofwd_type or 'users' in autofwd_type:
                                                                    autofwd_type_t += chat_type_persian['supergroups']
                                                                send_msg(chat_id, '❆ خواندن پیام ها (تیک دوم) : ' + ('✅' if db.get(profile + 'markread') else '❌') + '\n❆ عضویت خودکار : ' + ('❌' if db.get(profile + 'link_limit') else '✅') + '\n❆ عضویت اجباری : ' + ('✅' if db.get(profile + 'force_join') else '❌') + ' \n❆ کانال عضویت اجباری : ' + (db.get(profile + 'force_join') if db.get(profile + 'force_join') else 'خالی') + '\n❆ فروارد اتومات : ' + ('هر ' + str(db.get(profile + 'autofwd_time') or '') + ' ثانیه' if db.get(profile + 'autofwd_time') else '❌') + '\n❆ پست های در صف فروارد : ' + str(db.scard(profile + 'autofwd_list')) + '\n❆ مقصد فروارد اتومات : ' + autofwd_type_t + '\n❆ محدودیت تعداد اعضای گروه برای عضویت : ' + (str(db.get(profile + 'minjoincount') or '') if db.get(profile + 'minjoincount') else '❌'), m_id)
                                                            else:
                                                                if text == 'markread on':
                                                                    db.set(profile + 'markread', True)
                                                                    send_msg(chat_id, '⫸ تیک دوم ࿊فعال شد .')
                                                                else:
                                                                    if text == 'markread off':
                                                                        db.delete(profile + 'markread')
                                                                        send_msg(chat_id, '⫸ تیک دوم ࿊غیر فعال شد .')
                                                                    else:
                                                                        if text == 'info':
                                                                            #last_version = requests.get(host_url + '/getVersion.php').text
                                                                            update = ''
                                                                            '''
                                                                            if last_version == Version:
                                                                                update = '⫸ شما آخرین ورژن بی جی تبچی را نصب دارید ! ( ورژن ' + Version + ' )'
                                                                            else:
                                                                                update = '⫸ آخرین نسخه ی بیجی تبچی  `' + last_version + '` و نسخه ی بیجی تبچی شما `' + Version + '` می باشد توصیه میکنیم برای استفاده از تمامی امکانات تبچی با استفاده از دستور `Update` بیجی تبچی رو به آخرین نسخه بروز نمایید !'
                                                                            '''
                                                                            send_msg(chat_id, '<i>Stats & BoT Info</i>\n➖➖➖➖➖➖➖➖\n<b>•⇩ Stats ⇩•</b>\n\n• کانال ها : <code>' + str(db.scard(profile + 'pv_channels') + db.scard(profile + 'pub_channels')) + '</code>\n   -- کانال های عمومی : <code>' + str(db.scard(profile + 'pub_channels')) + '</code>\n   -- کانال های خصوصی : <code>' + str(db.scard(profile + 'pv_channels')) + '</code>\n• سوپرگروه ها : <code>' + str(db.scard(profile + 'pv_supergroups') + db.scard(profile + 'pub_supergroups')) + '</code>\n   -- سوپرگروه های عمومی : <code>' + str(db.scard(profile + 'pub_supergroups')) + '</code>\n   -- سوپرگروه های خصوصی : <code>' + str(db.scard(profile + 'pv_supergroups')) + '</code>\n• گروه ها : <code>' + str(db.scard(profile + 'groups')) + '</code>\n• کاربران(پیوی ها) : <code>' + str(db.scard(profile + 'users')) + '</code>\n• مخاطبین : <code>' + str(db.scard(profile + 'contacts')) + '</code>\n➖➖➖➖➖➖➖➖\n<b>•⇩ Info ⇩•</b>\n• لینک های جوین شده : <code>' + str(db.scard(profile + 'saved_links')) + '</code>\n• لینک های در صف جوین : <code>' + str(db.scard(profile + 'inwait_links')) + '</code>\n' + update + '\n➖➖➖➖➖➖➖➖\n<b>•⇩ About ⇩•</b>\n\n• شمارنده ربات : <code>' + str(profile) + '</code>\n• نام ربات : <code>' + Bot['first_name'] + '</code>\n• یوزر آیدی ربات : <code>' + str(Bot['id']) + '</code>\n• شماره اکانت ربات : <code>+' + Bot['phone_number'] + '</code>\n➖➖➖➖➖➖➖➖', m_id, 'html')

                                                                        else:
                                                                            if text and h.set(re.search('^send (all|groups|supergroups|channels|users|contacts) (.+)$', text)):
                                                                                printw('Sending Pm to ' + h.get().group(1) + '+ ... !')
                                                                                send_msg(chat_id, '❕ در حال ارسال پیام به تمامی ' + h.get().group(1))
                                                                                tt = time()
                                                                                type_list = list(db.smembers(profile + h.get().group(1))) + list(db.smembers(profile + 'pv_' + h.get().group(1))) + list(db.smembers(profile + 'pub_' + h.get().group(1)))
                                                                                for chat in type_list:
                                                                                    send_msg(chat, h.get().group(2), 0, 'html')

                                                                                send_msg(chat_id, '❕ پیام با موفقیت فرستاده شد!\n⏱ زمان ارسال: ' + timetostr(time() - tt))
                                                                            else:
                                                                                if text and h.set(re.search('^fwd (all|groups|supergroups|channels|users|contacts)$', text)) and m['reply_to_message_id'] != 0:
                                                                                    printw('Forwarding Pm to ' + h.get().group(1) + '+ ... !')
                                                                                    send_msg(chat_id, '❕ در حال فروارد پیام به تمامی ' + chat_type_persian[h.get().group(1)])
                                                                                    tt = time()
                                                                                    type_list = list(db.smembers(profile + h.get().group(1))) + list(db.smembers(profile + 'pv_' + h.get().group(1))) + list(db.smembers(profile + 'pub_' + h.get().group(1)))
                                                                                    for chat in type_list:
                                                                                        td_send('forwardMessages', {'chat_id': chat, 'from_chat_id': chat_id, 'message_ids': [m['reply_to_message_id']], 'disable_notification': True, 'from_background': True})

                                                                                    send_msg(chat_id, '❕ پیام با موفقیت فروارد شد!\n⏱ زمان ارسال: ' + timetostr(time() - tt))
                                                                                else:
                                                                                    if text and h.set(re.search('^send (\d+) (all|groups|supergroups|channels|users|contacts) (.+)$', text)):
                                                                                        count = int(h.get().group(1))
                                                                                        tt = time()
                                                                                        type_list = list(db.smembers(profile + h.get().group(2))) + list(db.smembers(profile + 'pv_' + h.get().group(2))) + list(db.smembers(profile + 'pub_' + h.get().group(2)))
                                                                                        if count > len(type_list):
                                                                                            count = len(type_list)
                                                                                        type_list = random.sample(type_list, count)
                                                                                        printw('Sending Pm to ' + h.get().group(2) + '+ ... !')
                                                                                        send_msg(chat_id, '❕ در حال ارسال پیام به ' + str(count) + ' ' + chat_type_persian[h.get().group(2)])
                                                                                        for chat in type_list:
                                                                                            send_msg(chat, h.get().group(3), 0, 'html')

                                                                                        send_msg(chat_id, '❕ پیام با موفقیت فرستاده شد!\n⏱ زمان ارسال: ' + timetostr(time() - tt))
                                                                                    else:
                                                                                        if text and h.set(re.search('^fwd (\d+) (all|groups|supergroups|channels|users|contacts)$', text)) and m['reply_to_message_id'] != 0:
                                                                                            tt = time()
                                                                                            type_list = list(db.smembers(profile + h.get().group(2))) + list(db.smembers(profile + 'pv_' + h.get().group(2))) + list(db.smembers(profile + 'pub_' + h.get().group(2)))
                                                                                            if count > len(type_list):
                                                                                                count = len(type_list)
                                                                                            type_list = random.sample(type_list, count)
                                                                                            printw('Forwarding Pm to ' + h.get().group(2) + '+ ... !')
                                                                                            send_msg(chat_id, '❕ در حال فروارد پیام به ' + str(count) + ' ' + chat_type_persian[h.get().group(2)])
                                                                                            for chat in type_list:
                                                                                                td_send('forwardMessages', {'chat_id': chat, 'from_chat_id': chat_id, 'message_ids': [m['reply_to_message_id']], 'disable_notification': True, 'from_background': True})

                                                                                            send_msg(chat_id, '❕ پیام با موفقیت فروارد شد!\n⏱ زمان ارسال: ' + timetostr(time() - tt))
                                                                                        else:
                                                                                            if text == 'getlinks':
                                                                                                temp_name = tempfile.mktemp() + '.txt'
                                                                                                with open(temp_name, 'w') as (file):
                                                                                                    for link in db.smembers(profile + 'all_links'):
                                                                                                        file.write('https://t.me/joinchat/' + link + '\n')

                                                                                                    file.seek(0, 0)
                                                                                                td_send('sendMessage', {'chat_id': chat_id, 'reply_to_message_id': m_id, 'disable_notification': True, 'from_background': True, 'input_message_content': {'@type': 'inputMessageDocument', 'document': {'@type': 'inputFileLocal', 'path': temp_name}, 'thumbnail': None, 'caption': None}})
                                                                                                sleep(1)
                                                                                                os.unlink(temp_name)
                                                                                            else:
                                                                                                if text == 'resetlinks':
                                                                                                    db.delete(profile + 'all_links')
                                                                                                    db.delete(profile + 'saved_links')
                                                                                                    db.delete(profile + 'inwait_links')
                                                                                                    send_msg(chat_id, '⫸ تمامی لینک ها پاکسازی شدند !', m_id)
                                                                                                else:
                                                                                                    if text and h.set(re.search('^leave (groups|supergroups|channels)$', text)):
                                                                                                        chats = list(db.smembers(profile + h.get().group(1))) + list(db.smembers(profile + 'pv_' + h.get().group(1))) + list(db.smembers(profile + 'pub_' + h.get().group(1)))
                                                                                                        before = len(chats)
                                                                                                        i = 0
                                                                                                        for chat in chats:
                                                                                                            i += 1
                                                                                                            is_last = False
                                                                                                            if i == before:
                                                                                                                is_last = True
                                                                                                            td_send('setChatMemberStatus', {'chat_id': chat, 'user_id': Bot['id'], 'status': {'@type': 'chatMemberStatusLeft'}}, 'leave_chat', {'group': h.get().group(1), 'm': m, 'chat': chat, 'is_last': is_last, 'before': before})

                                                                                                    else:
                                                                                                        if text == 'joinlinks off':
                                                                                                            db.set(profile + 'link_limit', True)
                                                                                                            send_msg(chat_id, '⫸ عضویت خودکار ࿊ غیرفعال ࿊ شد .')
                                                                                                        else:
                                                                                                            if text == 'joinlinks on':
                                                                                                                db.delete(profile + 'link_limit')
                                                                                                                send_msg(chat_id, '⫸ عضویت خودکار ࿊ فعال ࿊ شد .')
                                                                                                            else:
                                                                                                                if text == 'addcontacts on':
                                                                                                                    db.delete(profile + 'contacts_limit')
                                                                                                                    send_msg(chat_id, '⫸ افزودن مخاطب ࿊ فعال ࿊ شد .\n✯ در تمامی گروه های تبچی اگر مخاطبی به اشتراک گذاشته شود ، توسط ربات به مخاطبان آن افزوده می شود !')
                                                                                                                else:
                                                                                                                    if text == 'addcontacts off':
                                                                                                                        db.set(profile + 'contacts_limit', True)
                                                                                                                        send_msg(chat_id, '⫸ افزودن مخاطب ࿊ غیرفعال ࿊ شد .')
                                                                                                                    else:
                                                                                                                        if text == 'addcontacts null':
                                                                                                                            db.delete(profile + 'addcontacts_text')
                                                                                                                            send_msg(chat_id, '⫸ پیام افزودن مخاطب حذف شد و افزودن مخاطب با پیام ࿊ غیرفعال ࿊ شد !')
                                                                                                                        else:
                                                                                                                            if text and h.set(re.search('^addcontacts (.+)$', text)):
                                                                                                                                db.set(profile + 'addcontacts_text', h.get().group(1))
                                                                                                                                send_msg(chat_id, '⫸ پیام افزودن مخاطب ذخیره و افزودن مخاطب با پیام ࿊ فعال ࿊ شد .\n✯ پیام افزودن مخاطب به ༜ "' + h.get().group(1) + '" ༜ تنظیم شد !')
                                                                                                                            else:
                                                                                                                                if text == 'badnames list':
                                                                                                                                    badnames_text = ('\n').join((str(x) for x in db.smembers(profile + 'badnames')))
                                                                                                                                    send_msg(chat_id, '⫸ لیست کلمات سیاه : ' + ('خالی' if badnames_text == '' else badnames_text))
                                                                                                                                else:
                                                                                                                                    if text and h.set(re.search('^badnames \+ (.+)$', text)):
                                                                                                                                        badname = h.get().group(1).lower()
                                                                                                                                        if db.sismember(profile + 'badnames', badname):
                                                                                                                                            send_msg(chat_id, '⫸ کلمه ی مورد نظر در لیست سیاه قرار دارد !')
                                                                                                                                        else:
                                                                                                                                            db.sadd(profile + 'badnames', badname)
                                                                                                                                            send_msg(chat_id, '⫸ کلمه ی مورد نظر به لیست سیاه اضافه شد و ازین به بعد تبچی در گروه هایی که این کلمه در اسم آن وجود دارد عضو نخواهد شد !')
                                                                                                                                    else:
                                                                                                                                        if text and h.set(re.search('^badnames \- (.+)$', text)):
                                                                                                                                            badname = h.get().group(1).lower()
                                                                                                                                            if not db.sismember(profile + 'badnames', badname):
                                                                                                                                                send_msg(chat_id, '⫸ کلمه ی مورد نظر در لیست سیاه قرار ندارد !')
                                                                                                                                            else:
                                                                                                                                                db.srem(profile + 'badnames', badname)
                                                                                                                                                send_msg(chat_id, '⫸ کلمه ی مورد نظر از لیست سیاه حذف شد !')
                                                                                                                                        else:
                                                                                                                                            if text == 'setmincount off':
                                                                                                                                                db.delete(profile + 'minjoincount')
                                                                                                                                                send_msg(chat_id, '⫸ محدودیت ࿊ اعضا ࿊ برای جوین شدن برداشته شد .')
                                                                                                                                            else:
                                                                                                                                                if text and h.set(re.search('^setmincount (\d+)$', text)):
                                                                                                                                                    db.set(profile + 'minjoincount', int(h.get().group(1)))
                                                                                                                                                    send_msg(chat_id, '⫸ از این پس تبچی در گروه هایی که اعضای آن کمتر از "' + h.get().group(1) + '" است , جوین نمی شود .')
                                                                                                                                                else:
                                                                                                                                                    if text == 'autofwd list':
                                                                                                                                                        send_msg(chat_id, '⫷ تمامی پست های موجود در لیست فروارد ⫸')
                                                                                                                                                        for post_data in db.smembers(profile + 'autofwd_list'):
                                                                                                                                                            m_idf, chat_idf = post_data.split(':')
                                                                                                                                                            td_send('forwardMessages', {'chat_id': chat_id, 'from_chat_id': chat_idf, 'message_ids': [m_idf], 'disable_notification': True, 'from_background': True})

                                                                                                                                                    else:
                                                                                                                                                        if text == 'autofwd +' and m['reply_to_message_id'] != 0:
                                                                                                                                                            post_data = str(m['reply_to_message_id']) + ':' + str(m['chat_id'])
                                                                                                                                                            if not db.sismember(profile + 'autofwd_list', post_data):
                                                                                                                                                                db.sadd(profile + 'autofwd_list', post_data)
                                                                                                                                                                send_msg(chat_id, '⫸ پیام مورد نظر شما به لیست ࿊ فروارد ࿊ اضافه شد .', m_id)
                                                                                                                                                            else:
                                                                                                                                                                send_msg(chat_id, '⫸ پیام مورد نظر شما در لیست ࿊ فروارد ࿊ موجود است !', m_id)
                                                                                                                                                        else:
                                                                                                                                                            if text == 'autofwd -' and m['reply_to_message_id'] != 0:
                                                                                                                                                                post_data = str(m['reply_to_message_id']) + ':' + str(m['chat_id'])
                                                                                                                                                                if db.sismember(profile + 'autofwd_list', post_data):
                                                                                                                                                                    db.srem(profile + 'autofwd_list', post_data)
                                                                                                                                                                    send_msg(chat_id, '⫸ پیام مورد نظر شما از لیست ࿊ فروارد ࿊ حذف شد .', m_id)
                                                                                                                                                                else:
                                                                                                                                                                    send_msg(chat_id, '⫸ پیام مورد نظر شما در لیست ࿊ فروارد ࿊ موجود نیست !', m_id)
                                                                                                                                                            else:
                                                                                                                                                                if text == 'autofwd clean':
                                                                                                                                                                    db.delete(profile + 'autofwd_list')
                                                                                                                                                                    send_msg(chat_id, '⫸ لیست پست های فروارد خودکار با موفقیت پاکسازی شد !', m_id)
                                                                                                                                                                else:
                                                                                                                                                                    if text == 'autofwd off':
                                                                                                                                                                        db.delete(profile + 'autofwd_time')
                                                                                                                                                                        db.set(profile + 'autofwd_limit', True)
                                                                                                                                                                        send_msg(chat_id, '⫸ فروارد اتومات ࿊ غیرفعال ࿊ شد .', m_id)
                                                                                                                                                                    else:
                                                                                                                                                                        if text and h.set(re.search('^autofwd (\d+)$', text)):
                                                                                                                                                                            fwdtime = h.get().group(1)
                                                                                                                                                                            db.set(profile + 'autofwd_time', fwdtime)
                                                                                                                                                                            db.setex(profile + 'autofwd_limit', fwdtime, True)
                                                                                                                                                                            send_msg(chat_id, '⫸ زمان بین هر فروارد به ' + str(fwdtime) + ' ثانیه تنظیم شد .', m_id)
                                                                                                                                                                        else:
                                                                                                                                                                            if text and h.set(re.search('^autofwd (.+)$', text)):
                                                                                                                                                                                autofwd_type = ''
                                                                                                                                                                                autofwd_type_t = h.get().group(1)
                                                                                                                                                                                if 'groups' in autofwd_type_t:
                                                                                                                                                                                    autofwd_type += 'groups'
                                                                                                                                                                                if 'supergroups' in autofwd_type_t:
                                                                                                                                                                                    autofwd_type += 'supergroups'
                                                                                                                                                                                if 'users' in autofwd_type_t:
                                                                                                                                                                                    autofwd_type += 'users'
                                                                                                                                                                                if autofwd_type != '':
                                                                                                                                                                                    db.set(profile + 'autofwd_type', autofwd_type)
                                                                                                                                                                                    send_msg(chat_id, '⫸ ازین پس پیام های در لیست فروارد اتومات به ࿊ ' + str(chat_type_persian[h.get().group(1)]) + ' ࿊ ارسال خواهد شد .', m_id)
                                                                                                                                                                            else:
                                                                                                                                                                                if text == 'forcejoin off':
                                                                                                                                                                                    db.delete(profile + 'force_join')
                                                                                                                                                                                    send_msg(chat_id, '⫸ جوین اجباری در کانال غیر فعال شد !')
                                                                                                                                                                                else:
                                                                                                                                                                                    if text and h.set(re.search('^forcejoin (@\S+)$', text)):
                                                                                                                                                                                        td_send('searchPublicChat', {'username': h.get().group(1)}, 'add_channel', {'m': m, 'username': h.get().group(1)})
                                                                                                                                                                                    else:
                                                                                                                                                                                        if text == 'addc' and m['reply_to_message_id'] != 0:
                                                                                                                                                                                            td_send('getMessage', {'chat_id': chat_id, 'message_id': m['reply_to_message_id']}, 'add_contact', m)
                                                                                                                                                                                        else:
                                                                                                                                                                                            if text == 'addmembers':
                                                                                                                                                                                                for user in db.smembers(profile + 'users'):
                                                                                                                                                                                                    td_send('addChatMember', {'chat_id': chat_id, 'user_id': user})

        else:
            if m['content']['@type'] == 'messageContact':
                if not db.get(profile + 'contacts_limit'):
                    if not db.sismember(profile + 'contacts', m['content']['contact']['user_id']):
                        td_send('importContacts', {'contacts': [m['content']['contact']]})
                        db.sadd(profile + 'contacts', m['content']['contact']['user_id'])
                        contacttext = db.get(profile + 'addcontacts_text')
                        if contacttext:
                            send_msg(chat_id, contacttext, m_id)
            else:
                if m['content']['@type'] == 'messageChatAddMembers':
                    for member in m['content']['member_user_ids']:
                        if int(member) == int(Bot['id']) and allready_gp(chat_id):
                            td_send('setChatMemberStatus', {'chat_id': chat_id,
                               'user_id': Bot['id'],
                               'status': {'@type': 'chatMemberStatusLeft'}})

                else:
                    if m['content']['@type'] == 'messageChatDeleteMember' and int(m['content']['user_id']) == int(Bot['id']):
                        td_send('deleteChatHistory', {'chat_id': chat_id, 'remove_from_chat_list': True})
                        chat_rem(chat_id)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print (exc_type, fname, exc_tb.tb_lineno, e)

    return


while True:
    event = td_receive()
    if event:
        if event['@type'] == 'updateAuthorizationState':
            if event['authorization_state']['@type'] == 'authorizationStateClosed':
                break
            else:
                if event['authorization_state']['@type'] == 'authorizationStateWaitTdlibParameters':
                    td_send('setTdlibParameters', {'parameters': {'use_test_dc': False, 'database_directory': 'Profiles/' + profile + '/datas', 'files_directory': 'Profiles/' + profile + '/files', 'use_file_database': True, 'use_chat_info_database': True, 'use_message_database': True, 'use_secret_chats': True, 'api_id': api_id, 'api_hash': api_hash, 'system_language_code': 'en', 'device_model': 'BGTeaM/Tab', 'system_version': 'Tab', 'application_version': '1.0', 'enable_storage_optimizer': True, 'ignore_file_names': True}})
                else:
                    if event['authorization_state']['@type'] == 'authorizationStateWaitEncryptionKey':
                        td_send('checkDatabaseEncryptionKey', {'encryption_key': ''})
                    else:
                        if event['authorization_state']['@type'] == 'authorizationStateWaitPhoneNumber':
                            td_send('setAuthenticationPhoneNumber', {'phone_number': raw_input('Phone : '), 'allow_flash_call': False, 'is_current_phone_number': False}, 'code_send')
                        else:
                            if event['authorization_state']['@type'] == 'authorizationStateWaitCode':
                                check_code(raw_input('Code : '), event['authorization_state']['is_registered'])
                            else:
                                if event['authorization_state']['@type'] == 'authorizationStateWaitPassword':
                                    check_password(raw_input('Pass(hint : ' + event['password_hint'] + ') : '))
                                else:
                                    if event['authorization_state']['@type'] == 'authorizationStateReady':
                                        printi('tabchi is ready!')
                                        '''
                                        version = db.get(profile + 'Version') or '1.0'
                                        if Version != version:
                                            send_msg(sudo, '⫸ بیجی تبچی با موفقیت به نسخه <code>' + Version + '</code> بروز شد .\n💡تغییرات آخرین نسخه :  \n💡<pre>' + requests.get(host_url + '/getDesc.php?v=' + Version).content + '</pre>', 0, 'html')
                                        db.set(profile + 'Version', Version)
                                        last_version = requests.get(host_url + '/getVersion.php').text
                                        '''
                                        update = ''
                                        '''
                                        if last_version == Version:
                                            update = '⫸ شما آخرین ورژن بی جی تبچی را نصب دارید ! ( ورژن ' + Version + ' )'
                                        else:
                                            update = '⫸ آخرین نسخه ی بیجی تبچی  `' + last_version + '` و نسخه ی بیجی تبچی شما `' + Version + '` می باشد توصیه میکنیم برای استفاده از تمامی امکانات تبچی با استفاده از دستور `Update` بیجی تبچی رو به آخرین نسخه بروز نمایید !'
                                        '''
                                        send_msg(sudo, '⫸ بیجی تبچی با موفقیت روشن شد .\n' + update, 0, 'markdown')
                                        td_send('getMe', {}, 'get_bot_info')
                                        check_stats()
                                        check_links()
                                        check_fwd()
        else:
            if '@extra' in event and 'call_back' in event['@extra'] and event['@extra']['call_back'] != None:
                event_c = dict(event)
                del event['@extra']
                call_backs(event_c['@extra']['call_back'], event_c['@type'] != 'error', event, event_c['@extra']['extra_data'])
            else:
                if event['@type'] == 'updateNewMessage':
                    new_message(event['message'], event['contains_mention'])

td_json_client_destroy(client)
