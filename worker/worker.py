import os
import json
import requests
from time import sleep
from subprocess import call
# Memo
# curl -I --cookie "sessionid=xxx" localhost:8000/gettask

def request(url, ctype='get', data=None):
    cmd = requests.post
    if ctype == 'get':
        cmd = requests.get
    return cmd(url, cookies=config, data=data)

with open("config.json", "r") as fp:
    config = json.load(fp)

while True:

    host = config["hostaddr"]
    _geturl = "http://{}/gettask/".format(host)
    _writeurl = "http://{}/writetask/".format(host)

    try:
        res = request(_geturl, 'get')
        if "login" in res.url:
            res = requests(res.url, 'post', data=config)
            config["sessionid"] = res.text
            res = request(_geturl, 'get')
            with open("config.json", "w+") as fp:
                fp.write(json.dumps(config, indent=4, sort_keys=True))

        if res.status_code != 204 or res.text != '':
            with open('tmp.py', 'w+') as ofp:
                ofp.write(res.text)
            with open('tmp.txt', 'w+') as ofp:
                call(['python', 'tmp.py'], stdout=ofp)
            with open('tmp.txt', 'rb') as ofp:
                out = ofp.read()
            print(os.listdir())
            res = request(_writeurl, 'post', {'content':out} )
            os.remove('tmp.py')
            os.remove('tmp.txt')
        else:
            sleep(5)

    finally:
        with open("config.json", "w+") as fp:
            fp.write(json.dumps(config, indent=4, sort_keys=True))