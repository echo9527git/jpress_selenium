"""
工具类
"""
import json
import os
import pickle
import random
import string
import time

import pyautogui
from PIL import Image, ImageDraw
from pytesseract import pytesseract

from lib.showapirequest import ShowapiRequest





class BasePage:
    def __init__(self,driver,black_list):
        self.driver = driver
        self.black_list = black_list
    def find_element(self,locator):
        '''
        基础页面类中封装自己的定位方法---具备异常处理逻辑
        :param locator: 一个元组定位符
        :return: 返回一个定位到的元素，因为需要对元素进行操作
        '''
        try:
            # WebDriverWait(self.driver,20).until(EC.visibility_of_element_located(locator))
            return self.driver.find_element(*locator) #可能会出现异常，如果不出现就直接return
        except:# 如果出现异常就对处理，思路是循环去黑名单中找一些异常弹框：广告、好评、升级、tips等
            handle_element_exception(self.driver,self.black_list)
            # 可能找了两次之后还是没有找到，那么可能需要调用本身进行递归处理
            # * 的作用其实就是把序列 locator 中的每个元素，当作位置参数传进去
            return self.find_element(*locator)

    def handle_element_exception(driver, black_list):
        '''
        异常处理逻辑，思路是循环去黑名单中找一些异常弹框：广告、好评、升级、tips等
        :param self:
        :param driver: webdriver
        :param black_list: 需要被处理的弹窗黑名单
        :return:
        '''
        # elements方法会强行等待隐式等待时间，会降低脚步执行速度，所以这个地方将隐式等待时间设置为0
        driver.implicitly_wait(0)

        for locator in black_list:
            # 在异常处理逻辑中不能再出现异常，所以使用elements
            elements = driver.find_elements(*locator)
            if len(elements) >= 1:  # 说明找到了元素
                elements[0].click()  # 找到了点击即可--点击的是黑名单里面的弹框
                print("%s 弹框出现" % str(locator))
                break
            else:  # 如果没有找到，打印日志即可
                print("%s not found" % str(locator))

            # # 者使用page_source是否包含黑名单中值来处理---效率更高
            # page_source = self.driver.page_source
            # if "image_cancle" in  page_source:
            #     self.driver.find_element(*locator).click()
            # elif "tips" in page_source:
            #     pass
            # elif "cancle" in page_source:
            #     pass
            # # TODO:异常处理逻辑待完善

        # 处理完成之后把隐式等待时间还原
        driver.implicitly_wait(10)

    def find_elements(self,locator):
        return self.driver.find_elements(*locator)

    def find_and_click(self,locator):
        '''
        定位并点击元素，点击的时候也有可能会抛异常，所以也需要异常处理
        :param locator: 一个元组定位符
        :return:
        '''
        try:
            self.find_element(locator).click()
        except:
            handle_element_exception(self.driver,self.black_list)
            # 处理了异常再查找点击
            self.find_element(*locator).click()


def get_window_dpr(driver):
    """
    获取屏幕缩放比例
    :param driver: webdriver对象
    :return: 屏幕缩放比例
    """
    dpr = driver.execute_script('return window.devicePixeRatio')
    return dpr


def get_element_location(element):
    """
    获取一个元素的坐标位置，左上顶点和右下顶点
    :param element: 已定位的以为webelement元素
    :return: 返回坐标位置的一个元组：(left_top_x,left__top_y,right_down_x,right_down_y)
    """
    left_top_x = element.location['x']
    left__top_y = element.location['y']
    right_down_x = element.size['width'] + left_top_x
    right_down_y = element.size['height'] + left__top_y
    return (left_top_x, left__top_y, right_down_x, right_down_y)


def crop_picture(driver, selector, raw_picture_name, save_picture_name):
    """
    在原图片中截取element元素图片并另存为save_picture_name
    :param raw_picture_name: 原图片名称
    :param element: 需要被截取的元素webelement
    :param save_picture_name: 截取之后保存的文件名称
    :return:
    """
    # 定位到图片并获取到图片的左上右下的xy坐标
    element = driver.find_element_by_css_selector(selector)
    left_top_x = element.location['x']
    left__top_y = element.location['y']
    right_down_x = element.size['width'] + left_top_x
    right_down_y = element.size['height'] + left__top_y
    # 获取屏幕的缩放比例
    dpr = driver.execute_script('return window.devicePixeRatio')
    # 抠图
    raw_image = Image.open(raw_picture_name)
    target_image = raw_image.crop((left_top_x * dpr, left__top_y * dpr, right_down_x * dpr, right_down_y * dpr))
    target_image.save(save_picture_name)


def get_verification_code_by_pytesseract(driver, selector):
    """
    使用pytesseract通过webdriver和验证码的定位器selector获取验证码
    :param driver: webdriver对象
    :param selector: 验证码的定位器selector
    :return: 验证码
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
    # 获取屏幕的缩放比例
    dpr = driver.execute_script('return window.devicePixeRatio')
    # 在截屏中抠出验证码图片并保存图片名称为当前时间戳.png
    raw_image = Image.open(raw_picture_name)
    target_image = raw_image.crop((left_top_x * dpr, left__top_y * dpr, right_down_x * dpr, right_down_y * dpr))
    code_picture_name = path + '\\' + str(time.time()) + ".png"
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


def get_verificationcode_by_showapi(appId, appSecret, typeId, driver, selector):
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
    # 获取屏幕的缩放比例
    dpr = driver.execute_script('return window.devicePixeRatio')
    # 在截屏中抠出验证码图片并保存图片名称为当前时间戳.png
    raw_image = Image.open(raw_picture_name)
    target_image = raw_image.crop((left_top_x * dpr, left__top_y * dpr, right_down_x * dpr, right_down_y * dpr))
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
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, number))

    return rand_str


def save_cookie(driver, path):
    """
    保存cookie到文件
    :param driver: webdriver对象
    :param path: 保存文件的路径
    :return:
    """
    with open(path, 'wd') as filehandler:
        # 在哪个页面就获取它的cookie
        cookies = driver.get_cookies()
        pickle.dump(cookies, filehandler)


def load_cookie(driver, path):
    """
    加载cookie到webdriver
    :param driver: webdriver对象
    :param path: 保存有cookie的文件
    :return:
    """
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)


def click_by_pyautogui(element, x=0, y=0):
    """
    通过pyautogui实现元素点击
    :param element: webelement对象
    :param x: 点击时x坐标偏移量
    :param y: 点击时y坐标偏移量
    :return:
    """
    rect = element.rect
    # pyautogui.click(rect['x']+10,rect['y']+120)
    pyautogui.click(rect['x'] + x, rect['y'] + y)


def print_json(j):
    """
    json数据打印格式化
    :param j: json类型的json对象
    :return:
    """
    print(json.dumps(j.json(), indent=2, ensure_ascii=False))


def handle_element_exception(driver, black_list):
    '''
    异常处理逻辑，思路是循环去黑名单中找一些异常弹框：广告、好评、升级、tips等
    :param self:
    :param driver: webdriver
    :param black_list: 需要被处理的弹窗黑名单
    :return:
    '''
    # elements方法会强行等待隐式等待时间，会降低脚步执行速度，所以这个地方将隐式等待时间设置为0
    driver.implicitly_wait(0)

    for locator in black_list:
        # 在异常处理逻辑中不能再出现异常，所以使用elements
        elements = driver.find_elements(*locator)
        if len(elements) >= 1:  # 说明找到了元素
            elements[0].click()  # 找到了点击即可--点击的是黑名单里面的弹框
            print("%s 弹框出现" % str(locator))
        else:  # 如果没有找到，打印日志即可
            print("%s not found" % str(locator))

        # # 者使用page_source是否包含黑名单中值来处理---效率更高
        # page_source = self.driver.page_source
        # if "image_cancle" in  page_source:
        #     self.driver.find_element(*locator).click()
        # elif "tips" in page_source:
        #     pass
        # elif "cancle" in page_source:
        #     pass
        # # TODO:异常处理逻辑待完善

    # 处理完成之后把隐式等待时间还原
    driver.implicitly_wait(10)


def highlight_element_appium(imgelement, driver, original_name, target_name):
    """
    对指定元素标记高亮
    :param imgelement: 需要高亮的元素
    :param driver: webdriver对象
    :param original_name: 任意的一个图片名称
    :param target_name: 最后被高亮显示的图片名称
    :return:
    """
    # TODO：图片的路径及文件名称处理
    # original_name = "\screenpic\\"+original_name
    # target_name = "\screenpic\\" + target_name
    # 保存截图
    driver.get_screenshot_as_file(original_name)
    # 打开图片资源
    img = Image.open(original_name)
    draw = ImageDraw.Draw(img)
    location = imgelement.location  # 获取左上角起始坐标
    size = imgelement.size  # 获取元素的长宽
    # {'x': 195, 'y': 1608}
    # {'height': 58, 'width': 690}
    # # 253,2298----885,1666 -------X是横轴，Y是纵轴，起点为左上角顶点
    # x1, y1, x2, y2 = 195, 1608, 885, 1666  #
    # draw.rectangle([x1, y1, x2, y2], outline=(255, 0, 0), width=10)  # x1,y1左上定点，x2，y2右下顶点
    x1, y1 = location['x'], location['y']
    x2, y2 = location['x'] + size['width'], location['y'] + size['height']
    # 在空间区域画矩形
    draw.rectangle([x1, y1, x2, y2], outline=(255, 0, 0), width=10)
    # 重新保存标记高亮的图片
    img.save(target_name, format('PNG'))
    # 删除最开始保存的截图
    if os.path.exists(original_name):
        os.remove(original_name)
        print("删除未高亮截图成功" + original_name)
    else:
        print(original_name + "文件不存在")
    print("标记" + original_name + "高亮成功")

def highlight_element_selenium(driver, element):
    """
    高亮显示页面元素
    使用javascript代码将传入的页面元素对象的背景颜色和边框颜色分别设置为绿色和红色
    :param driver:
    :param element:
    :return:
    """
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                          "background:green; border:2px solid red;")


if __name__ == '__main__':
    code = get_verification_code_by_picture('timg.jpg')
    print(code)
