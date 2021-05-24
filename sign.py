import requests, time, random
import json
import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S')


# seq的1,2,3代表着早，中，晚
def get_seq():
    current_hour = datetime.datetime.utcnow()
    current_hour = current_hour.hour
    if 8 <= current_hour < 18:
        return 1
    elif 19 <= current_hour < 23:
        return 2
    elif 0 <= current_hour < 7:
       return 3
    else: 
      return 0


# 封装HTTP请求
def http_post(url, headers={}, data={}, retry=3):
    for i in range(retry):
        try:
            res = requests.post(url, headers=headers, data=data)
            return res
        except Exception as e:
            logging.error("post请求错误: %s" % e)
            logging.info('将在 100 秒后重新发起请求...')
            time.sleep(100)
    logging.error("本次发送请求失败！")


# server酱提醒
class Remind:
    sckey = False
    url = ""
    data = {
        "text": "校园签到打卡小助手-打卡",
        "desp": ""
    }

    def __init__(self, sckey):
        self.sckey = sckey
        self.url = "https://sc.ftqq.com/{}.send".format(sckey)

    def send_msg(self):
        res = http_post(self.url, data=self.data)
        result = json.loads(res.text)['errmsg']
        if result == 'success':
            logging.info("推送消息成功: {}".format(res.text))
        else:
            logging.info("推送消息失败了: {}".format(res.text))

    def success(self, desp):
        if not sckey.startswith('SC'):
            logging.warning('未正确配置SCKEY,跳过推送...')
            return
        self.data['text'] += '成功'
        self.data['desp'] = desp
        self.send_msg()

    def fail(self, desp):
        if not sckey.startswith('SC'):
            logging.warning('未正确配置SCKEY,跳过推送...')
            return
        self.data['text'] += '失败'
        self.data['desp'] = desp
        self.send_msg()


class Req:
    headers = {
        "Host": "student.wozaixiaoyuan.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Connection": "keep-alive",
        "charset": "utf-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "Referer": "https://servicewechat.com/wxce6d08f781975d91/172/page-frame.html",
        "token": "13e6abb6-1f79-48cf-a9ec-d819315b1f47",  # token
        # "Content-Length": "211"
    }

    def __init__(self, arg):
        self.headers['token'] = arg

    # 获取随机体温
    @staticmethod
    def get_random_temperature():
        random.seed(time.ctime())
        return "{:.1f}".format(random.uniform(36.2, 36.8))

    # 处理打卡结果
    @staticmethod
    def handle_res(res):
        if res and res['code'] == 0:
            logging.info("自动打卡签到结果 : code = {}".format(res['code']))
            Remind(sckey).success(" ^_^已经自动为您打卡成功啦~ ")
        elif res and res['code'] == -10:
            logging.error("打卡失败,TOKEN已过期,时间:{}".format(datetime.datetime.now()))
            Remind(sckey).fail(" @_@由于TOKEN过期失效,打卡失败了哦,请及时处理~ ")
        else:
            logging.error("打卡失败,时间:{}".format(datetime.datetime.now()))
            logging.error("打卡失败,时间:{}",res)
            Remind(sckey).fail(" @_@非常遗憾的通知您,打卡失败了哦,请及时处理~ ")


# 晨午检打卡
class Inspect(Req):
    saveUrl = "https://student.wozaixiaoyuan.com/heat/save.json"
    data = {
        "answers": '["0"]',
        "seq": 0,
        "temperature": 36.5,
        "userId": "",
        "latitude": "23.08331",
        "longitude": "113.3172",
        "country": "中国",
        "city": "广州市",
        "district": "海珠区",
        "province": "广东省",
        "township": "江海街道",
        "street": "上冲中约新街一巷",
        "myArea": "",
        "areacode":440105
    }

    # 提交打卡请求
    def submit_insp(self):
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"
        self.data['temperature'] = Req.get_random_temperature()
        res = http_post(self.saveUrl, headers=self.headers, data=self.data).json()
        self.handle_res(res)


# 晚签到
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

    # 获取签到ID
    def get_signID(self):
        data = {
            'page': '1',
            'size': '5'
        }
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"
        res = http_post(self.listUrl, headers=self.headers, data=data).json()
        if res and res['code'] == -10:
            logging.error("打卡失败,TOKEN已过期,时间:{}".format(datetime.datetime.now()))
            Remind(sckey).fail(" @_@由于TOKEN过期失效,打卡失败了哦,请及时处理~ ")
            return False
        else:
            self.data["id"] = res['data'][0]['logId']
            self.data["signId"] = res['data'][0]['id']
            return True

    # 提交签到请求
    def submit_sign(self):
        id_res = self.get_signID()
        if id_res:
            self.headers['Content-Type'] = "application/json"
            res = http_post(self.signUrl, headers=self.headers, data=json.dumps(self.data)).json()
            self.handle_res(res)


def main(token):
    seq = get_seq()
    if seq == 1 or seq == 2 or seq == 3:
        Inspect.data['seq'] = seq
        Inspect(token).submit_insp()
#    elif seq == 3:
#        Sign(token).submit_sign()
    else:
        logging.warning("当前不在签到时间!")
    return


if __name__ == "__main__":
    secret = input().strip().split('#')
    secret.append('')
    token = secret[0]
    sckey = secret[1]
    seconds = random.randint(10, 30)
    logging.info('将在 {} 秒后开始任务...'.format(seconds))
    time.sleep(seconds)
    main(token)
