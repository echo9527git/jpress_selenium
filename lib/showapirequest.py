import requests
from urllib import parse
#全局请求头
files = {}
headers = {}
body = {}
timeouts = {}
resHeader = {}

class ShowapiRequest:
    def __init__(self, url, my_appId, my_appSecret):
        self.url = url
        self.my_appId = my_appId
        self.my_appSecret = my_appSecret
        body["showapi_appid"] = my_appId
        body["showapi_sign"] = my_appSecret
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2427.7 Safari/537.36"

    def addFilePara(self, key, value_url):
        files[key] = open(r"%s" % (value_url), 'rb')
        return self

    def addHeadPara(self, key, value):
        headers[key] = value
        return self

    def addBodyPara(self, key, value):
        body[key] = value
        return self
    #设置连接时间和读取时间
    def setTimeout(self, connecttimout, readtimeout):
        timeouts["connecttimout"] = connecttimout
        timeouts["readtimeout"] = readtimeout
        return self


    def get(self):
        get_url = self.url + "?" + parse.urlencode(body)
        if not timeouts:
            res = requests.get(get_url, headers=headers)
        else:
            timeout = (timeouts["connecttimout"], timeouts["readtimeout"])
            res = requests.get(get_url, headers=headers, timeout=timeouts)
        return res

    def post(self):
        if not timeouts:
            res = requests.post(self.url, files=files, data=body, headers=headers)
        else:
            timeout = (timeouts["connecttimout"], timeouts["readtimeout"])
            res = requests.post(self.url, files=files, data=body, headers=headers, timeout=timeout)
        return res

if __name__ == '__main__':
    # 生成图片的对象：
    # image = Image.open("C:/我的代码/selenium自动化测试/Selenium3 与 Python3 实战 Web自动化测试框架/imooc2.png")
    # 使用图片转换成文字：
    # text = pytesseract.image_to_string(image)
    # print(text)
    r = ShowapiRequest("http://route.showapi.com/184-4", "329067", "a012ddfa683d405e9fa6b6b8745eac43")
    r.addBodyPara("typeId", "34")
    r.addBodyPara("convert_to_jpg", "0")
    r.addBodyPara("needMorePrecise","0")
    # 定义文件上传设置：
    # r.addFilePara("image", r"C:/我的代码/selenium自动化测试/Selenium3 与 Python3 实战 Web自动化测试框架/imooc1.png")
    r.addFilePara("image","test2.jpg")
    res = r.post()
    print("res=",res.json())
    text = res.json()['showapi_res_body']['Result']
    print(text)  # 返回信息