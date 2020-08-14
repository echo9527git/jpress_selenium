"""
selenium工具类
"""
import os
import pickle
import random
import string
import time

from PIL import Image
from pytesseract import pytesseract

from lib.showapirequest import ShowapiRequest


def get_element_location(element):
    """
    获取一个元素的坐标位置，左上顶点和右下顶点
    :param element: 已定位的以为webelement元素
    :return: 返回坐标位置的一个元组：(left_top_x,left__top_y,right_down_x,right_down_y)
    """
    left_top_x = element.location['x']
    left__top_y = element.location['y']
    right_down_x =element.size['width'] + left_top_x
    right_down_y = element.size['height'] + left__top_y
    return (left_top_x,left__top_y,right_down_x,right_down_y)

def crop_picture(raw_picture_name,element,save_picture_name):
    """
    在原图片中截取element元素图片并另存为save_picture_name
    :param raw_picture_name: 原图片名称
    :param element: 需要被截取的元素webelement
    :param save_picture_name: 截取之后保存的文件名称
    :return:
    """
    left_top_x = element.location['x']
    left__top_y = element.location['y']
    right_down_x = element.size['width'] + left_top_x
    right_down_y = element.size['height'] + left__top_y
    raw_image = Image.open(raw_picture_name)
    target_image = raw_image.crop((left_top_x,left__top_y,right_down_x,right_down_y))
    target_image.save(save_picture_name)

def get_verification_code_by_pytesseract(driver,selector):
    """
    使用pytesseract通过webdriver和验证码的定位器selector获取验证码
    :param driver: webdriver对象
    :param selector: 验证码的定位器selector
    :return: 验证码
    """
    # 获取screenshot文件夹路径
    path = os.path.dirname(os.path.dirname(__file__))+'\\screenshot'
    # 截屏保存并保存图片名称为当前时间戳.png
    raw_picture_name = path+'\\'+str(time.time())+".png"
    driver.save_screenshot(raw_picture_name)
    # 定位到验证码图片并获取到图片的左上右下的xy坐标
    element = driver.find_element_by_css_selector(selector)
    left_top_x = element.location['x']
    left__top_y = element.location['y']
    right_down_x = element.size['width'] + left_top_x
    right_down_y = element.size['height'] + left__top_y
    # 在截屏中抠出验证码图片并保存图片名称为当前时间戳.png
    raw_image = Image.open(raw_picture_name)
    target_image = raw_image.crop((left_top_x, left__top_y, right_down_x, right_down_y))
    code_picture_name = path+'\\'+str(time.time())+".png"
    target_image.save(code_picture_name)
    # 使用pytesseract获取图片中的验证码
    code_image = Image.open(code_picture_name)
    verification_code = pytesseract.image_to_string(code_image)
    return verification_code


def get_verification_code_by_picture(code_picture):
    """
    根据一张图片验证码图片获取到图片中的验证码内容
    :param code_picture: 图片验证码图片
    :return: 返回图片中的验证码
    """
    code_image = Image.open(code_picture)
    verification_code = pytesseract.image_to_string(code_image)
    return verification_code

def get_verificationcode_by_showapi(appId,appSecret,typeId,driver,selector):
    """
    通过万维易源的API来解决复杂验证码问题--需要提前在万维易源注册获取到appId和appSecret，并且需要购买之后才能使用
    :param appId: showapi_appId--在控制台-->我的应用中查看
    :param appSecret:showapi_appSecret--在控制台-->我的应用中查看
    :param typeId:图片中验证码字符的个数-->在showapi文档中查看
    :param pictureName:图片验证码图片名称
    :return:返回图片中验证码
    """
    # 获取screenshot文件夹路径
    path = os.path.dirname(os.path.dirname(__file__)) + '\\screenshot'
    # 截屏保存并保存图片名称为当前时间戳.png
    raw_picture_name = path + '\\' + str(time.time()) + ".png"
    driver.save_screenshot(raw_picture_name)
    # 定位到验证码图片并获取到图片的左上右下的xy坐标
    element = driver.find_element_by_css_selector(selector)
    left_top_x = element.location['x']
    left__top_y = element.location['y']
    right_down_x = element.size['width'] + left_top_x
    right_down_y = element.size['height'] + left__top_y
    # 在截屏中抠出验证码图片并保存图片名称为当前时间戳.png
    raw_image = Image.open(raw_picture_name)
    target_image = raw_image.crop((left_top_x, left__top_y, right_down_x, right_down_y))
    code_picture_name = path + '\\' + str(time.time()) + ".png"
    target_image.save(code_picture_name)
    # 通过showapi识别图中验证码
    r = ShowapiRequest("http://route.showapi.com/184-4", appId, appSecret)
    r.addBodyPara("typeId", typeId)
    r.addBodyPara("convert_to_jpg", "0")
    r.addBodyPara("needMorePrecise", "0")
    # 定义文件上传设置：
    # r.addFilePara("image", r"C:/我的代码/selenium自动化测试/Selenium3 与 Python3 实战 Web自动化测试框架/imooc1.png")
    r.addFilePara("image", code_picture_name)
    res = r.post()
    print("res=", res.json())
    verification_code = res.json()['showapi_res_body']['Result']
    return verification_code

def gen_random_str(number):
    """
    生成任意个数的字母和数字的组合
    :param number: 需要生成组合的字符个数
    :return: 返回一个字母和数字的组合
    """
    rand_str = ''.join(random.sample(string.ascii_letters+string.digits,number))
    return rand_str

def save_cookie(driver,path):
    """
    保存cookie到文件
    :param driver: webdriver对象
    :param path: 保存文件的路径
    :return:
    """
    with open(path,'wd') as filehandler:
        cookies = driver.get_cookies()
        pickle.dump(cookies,filehandler)

def load_cookie(driver,path):
    """
    加载cookie到webdriver
    :param driver: webdriver对象
    :param path: 保存有cookie的文件
    :return:
    """
    with open(path,'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

if __name__ == '__main__':
    code = get_verification_code_by_picture('timg.jpg')
    print(code)