import requests, time, random
import json
import datetime


# 我在校园token
#token = "d1b6f1e7-ce81-469e-8429-0c13b364143d"


# seq的1,2,3代表着早，中，晚
def get_seq():
    current_hour = datetime.datetime.now()
    current_hour = current_hour.hour
    if 6 <= current_hour <= 10:
        return 1
    elif 11 <= current_hour < 15:
        return 2
    elif 22 <= current_hour < 23:
        return 3
    else:
        return 0


def http_post(url, headers={}, data={}, retry=3):
    for i in range(retry):
        try:
            res = requests.post(url, headers=headers, data=data)
            return res
        except Exception as e:
            print("post请求错误: %s" % e)
            time.sleep(100)
    print("本次请求失败！")


class Remind:
    url = ""
    data = {
        "text": "校园签到打卡小助手-打卡",
        "desp": ""
    }

    def __init__(self, sckey):
        self.url = "https://sc.ftqq.com/{}.send".format(sckey)
    
    def success(self,desp):
        self.data['text']+='成功'
        self.data['desp'] = desp
        res = http_post(self.url, data=self.data)
        print(res, res.text)

    def fail(self,desp):
        self.data['text']+='失败'
        self.data['desp'] = desp
        res = http_post(self.url, data=self.data)
        print(res, res.text)


class Req:
    headers = {
        "Host": "student.wozaixiaoyuan.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Connection": "keep-alive",
        "charset": "utf-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "Referer": "https://servicewechat.com/wxce6d08f781975d91/155/page-frame.html",
        "token": "",  # 此处填写token
        #"Content-Length": "211"
    }
    
    def __init__(self,arg):
        self.headers['token'] = arg

    # 获取随机体温
    @staticmethod
    def get_random_temprature():
        random.seed(time.ctime())
        return "{:.1f}".format(random.uniform(36.2, 36.7))


class Inspect(Req):
    saveUrl = "https://student.wozaixiaoyuan.com/heat/save.json"
    data = {
        "answers": '["0"]',
        "seq": 0,
        "temperature": 36.5,
        "userId":"",
        "latitude":"",
        "longitude":"",
        "country":"",
        "city":"",
        "district":"",
        "province":"",
        "township":"",
        "street":"",
        "myArea":""
    }

    def submit_insp(self):
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"
        self.data['temperature'] = Req.get_random_temprature()
        res = http_post(self.saveUrl,headers=self.headers,data=self.data).json()
        if res and res['code'] == 0:
            print("晨午检打卡结果 : code = ", res['code'])
            Remind(sckey).success(" ^_^已经自动为您打卡成功啦~ \n 体温:"+str(self.data['temperature']))
        else:
            print("打卡失败,时间:",datetime.datetime.now())
            Remind(sckey).fail(" @_@非常遗憾的通知您,签到失败了哦,请及时处理~ ")

class Sign(Req):
    listUrl = "https://student.wozaixiaoyuan.com/sign/getSignMessage.json"
    signUrl = "https://student.wozaixiaoyuan.com/sign/doSign.json"

    data = {
        "id": "",
        "signId": "",
        "latitude": 34.102702,
        "longitude": 108.653637,
        "country": "中国",
        "province": "陕西省",
        "city": "西安市",
        "district": "鄠邑区",
        "township": "五竹街道"
    }

    def get_signID(self):
        data = {
            'page': '1',
            'size': '5'
        }
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"
        res = http_post(self.listUrl,headers=self.headers,data=data).json()
        if res:
            self.data["id"] = res['data'][0]['logId']
            self.data["signId"] = res['data'][0]['id']
            return True

    def submit_sign(self):
        id_res = self.get_signID()
        if id_res:
            self.headers['Content-Type'] = "application/json"
            res = http_post(self.signUrl,headers=self.headers,data=json.dumps(self.data)).json()
            if res and res['code'] == 0:
                print("签到结果 : code = ", res['code'])
                Remind(sckey).success(" ^_^已经自动为您签到成功啦~ ")
            else:
                print("签到失败,时间:",datetime.datetime.now())
                Remind(sckey).fail(" @_@非常遗憾的通知您,签到失败了哦,请及时处理~ ")


def main(token):
    seq = get_seq()
    if seq == 1 or seq == 2:
        Inspect.data['seq'] = seq
        Inspect(token).submit_insp()
    elif seq == 3:
        Sign(token).submit_sign()
    else:
        print("当前不在签到时间!")
        return


if __name__ == "__main__":
    secret = input().strip().split('#')
    secret.append('')
    token = secret[0]
    sckey = secret[1]
    seconds = random.randint(10, 30)
    print('将在 {} 秒后开始任务...'.format(seconds))
    time.sleep(seconds)
    main(token)
