import itchat
import json
import time
import pathlib
import requests
import re

sex_dict = {}
sex_dict['0'] = "其他"
sex_dict['1'] = "男"
sex_dict['2'] = "女"

def save_data(friends_list):
    ''' save friends data into file
    '''
    path=pathlib.Path("friends")
    if path.exists():#os.path.exists("friends")
        pass
    else:
        path.mkdir()# os.mkdir("friends")

    path=path/"info.txt"
    if path.exists() and path.is_file():
        print(path.read_text(encoding="utf-8"))
    else:
        path.write_text(json.dumps(friends_list,ensure_ascii=False),encoding="utf-8")

def get_head_img(HeadImgUrl):
    ''' modify the itchat module:
        add interface to get cookies from it
    '''
    sessionClient = requests.Session()# session会话，requets复杂用法，保持cookie
    sessionClient.cookies = requests.utils.cookiejar_from_dict(itchat.get_cookies())
    # you can use params or use the url which contains params directly
    # url = "https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxgeticon"
    # res = re.match("/cgi-bin/mmwebwx-bin/webwxgeticon\?seq=(\d+)&username=(@[\d|\w]+)&skey=(.*)", HeadImgUrl)
    # params = {
    #     "seq": res.group(1),
    #     "username": res.group(2),
    #     "skey": res.group(3),
    #     'type': 'big',
    # }
    url = "https://wx2.qq.com" + HeadImgUrl+"&type=big"
    headers = {
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Host": "wx2.qq.com",
        "Referer": "https://wx2.qq.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    # print("get: url={0} params={1}".format(url, json.dumps(params)))
    # resp = sessionClient.get(url, params=params, stream=True, headers=headers)
    with sessionClient.get(url, stream=True, headers=headers) as resp:
        print(resp.headers)
        with open("friends/img/Hello.jpg", "wb") as file:
            for block in resp.iter_content(chunk_size=1024):
                file.write(block)

def download_images(friends_list):
    path=pathlib.Path("friends/images")
    if path.exists():
        pass
    else:
        path.mkdir()

    for friend in friends_list:
        img = itchat.get_head_img(userName=friend["UserName"])# get_head_img: requests.Session()  一次会话，not requests.get()
        with open("friends/images/"+friend['UserName']+".jpg", 'wb') as file:
            file.write(img)

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)

    friends = itchat.get_friends(update=True)[0:]#获取好友信息
    friends_list = []

    for friend in friends:
        item = {}
        item['NickName'] = friend['NickName']
        item['HeadImgUrl'] = friend['HeadImgUrl']
        item['Sex'] = sex_dict[str(friend['Sex'])]
        item['Province'] = friend['Province']
        item['Signature'] = friend['Signature']
        item['UserName'] = friend['UserName']

        friends_list.append(item)
        # print(item)

    # save_data(friends_list)
    # download_images(friends_list)

    user = itchat.search_friends(name='赵志昆')[0]
    get_head_img(user['HeadImgUrl'])

    time.sleep(3)
    # itchat.logout()
