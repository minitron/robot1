# coding: utf-8
import os
import sys
import re
import json
import time
import urllib.request, urllib.parse, urllib.error
import logging


class Robot(object):

    def __init__(self):
        # read file ini.txt
        ini_path = os.path.abspath('.')
        ini_filename = ini_path + '/data/ini.txt'
        with open(ini_filename, 'rt', encoding='utf-8') as f:
            for line in f:
                self.config = line
        # read file line and set config
        self.config = line
        self.appid = 'wx782c26e4c19acffb'
        self.lang = 'zh_CN'

    def _echo(self, str):
        sys.stdout.write(str)
        sys.stdout.flush()

    def _post(self, url: object, params: object, jsonfmt: object = True) -> object:
        if jsonfmt:
            data = (json.dumps(params)).encode()

            request = urllib.request.Request(url=url, data=data)
            request.add_header(
                'ContentType', 'application/json; charset=UTF-8')
        else:
            request = urllib.request.Request(url=url, data=urllib.parse.urlencode(params).encode(encoding='utf-8'))

        try:
            response = urllib.request.urlopen(request)
            data = response.read()
            if jsonfmt:
                return json.loads(data.decode('utf-8'))  # object_hook=_decode_dict)
            return data
        except urllib.error.HTTPError as e:
            logging.error('HTTPError = ' + str(e.code))
        except urllib.error.URLError as e:
            logging.error('URLError = ' + str(e.reason))
        except http.client.HTTPException as e:
            logging.error('HTTPException')
        except Exception:
            import traceback
            logging.error('generic exception: ' + traceback.format_exc())

        return ''

    def getUUID(self):
        url = 'https://login.weixin.qq.com/jslogin'
        params = {
            'appid': self.appid,
            'fun': 'new',
            'lang': self.lang,
            '_': int(time.time()),
        }
        data = self._post(url, params, False).decode("utf-8")
        if data == '':
            return False
        regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
        pm = re.search(regx, data)
        if pm:
            code = pm.group(1)
            self.uuid = pm.group(2)
            return code == '200'
        return False

    def _run(self, str, func, *args):
        self._echo(str)
        if func(*args):
            print('成功')
            logging.debug('%s... 成功' % (str))
        else:
            print('失败\n[*] 退出程序')
            logging.debug('%s... 失败' % (str))
            logging.debug('[*] 退出程序')
            exit()

    def start(self):
        # connect wx server
        self._echo('[*] 微信网页版 ... 开动\n')
        self._run('[*] 正在获取 uuid ... ', self.getUUID)
        self._echo('[*] 正在获取二维码 ... 成功')

if __name__ == '__main__':
    Robot1 = Robot()
    Robot1.start()