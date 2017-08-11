import os
import json
import requests
from time import sleep
import subprocess 

def request(url, ctype='get', data=None):
    cmd = requests.post
    if ctype == 'get':
        cmd = requests.get
    return cmd(url, cookies=config, data=data)

with open("config.json", "r") as fp:
    config = json.load(fp)

max_try_connect = 5
n_try_connect = 0

while n_try_connect < max_try_connect:

    host = config["hostaddr"]
    _geturl = "http://{}/gettask/".format(host)
    _writeurl = "http://{}/writetask/".format(host)

    try:
        # print('Attemp to ask for new task from {}'.format(host))
        res = request(_geturl, 'get')
        n_try_connect = 0
        if "login" in res.url:
            # print('Session expire, attemp to re-login')
            res = request(res.url, 'post', data=config)
            if res.status_code == 400:
                # print()
                # print('***********************************************')
                # print()
                # print('!!! F A I L   T O   L O G I N.')
                # print()
                # print(' Please check config.json Or contact to admin.')
                # print()
                # print('***********************************************')
                # print()
                break
            config["sessionid"] = res.text
            res = request(_geturl, 'get')
            with open("config.json", "w+") as fp:
                fp.write(json.dumps(config, indent=4, sort_keys=True))

        if res.status_code != 204 or res.text != '':
            # print('\tGet new task')
            with open('tmp.py', 'w+') as ofp:
                ofp.write(res.text)
            with open('tmp.txt', 'w+') as ofp:
                p1 = subprocess.Popen(['cat', 'tmp.py'], stdout=subprocess.PIPE)
                p2 = subprocess.Popen(['docker', 'run', '-i', 'tfworker'], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p2.communicate()
                print(out)
                print()
                print(err)
            res = request(_writeurl, 'post', {'content':'{}\n{}'.format(out.decode('utf8'), err.decode('utf8'))} )
            os.remove('tmp.py')
            os.remove('tmp.txt')
        else:
            sleep(5)

    except requests.exceptions.ConnectionError as err:
        n_try_connect += 1
        sleep(1)


    finally:
        with open("config.json", "w+") as fp:
            fp.write(json.dumps(config, indent=4, sort_keys=True))
    # print('-'*40)
    # print()
# else:
    # print('Maximum attemp to connect {}'.format(host))
    # print('Please contact to admin')
