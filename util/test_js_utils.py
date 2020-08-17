import time
from selenium.webdriver.remote.webdriver import WebDriver
import unittest
from selenium import webdriver

from js_demo.js_utils import CssElement

# https://www.cnblogs.com/linuxchao/p/linuxchao-js.html
# https://blog.csdn.net/weixin_42170439/article/details/90645816
# https://www.cnblogs.com/yzyj/p/10425824.html

class Base(object):
    # window = CssElement

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def load_url(self, url):
        return self.driver.get(url)


class BaiDuPage(Base):
    search_input = CssElement("#kw", describe="百度搜索框")
    search_button = CssElement("#su", describe="百度按钮")

    def search(self):
        self.search_input.height_light()
        self.search_input.clear()
        time.sleep(2)  # 为了看到效果
        self.search_input.input("linux超")
        time.sleep(2)
        self.search_button.height_light()
        self.search_button.click()
        time.sleep(2)
        self.window.scrollTo("0", "500")
        time.sleep(10)  # 为了看到效果


class ChinaRailway(Base):
    data_input = CssElement("#train_date", describe="日期控件")

    def input_date(self, date):
        self.data_input.height_light()
        self.data_input.remove_attribute("readonly")
        self.data_input.input(date)
        time.sleep(2)  # 为了看到效果


class TestJs(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        self.bai_du_page = BaiDuPage(self.driver)
        self.china_railway = ChinaRailway(self.driver)

    def test_search(self):
        """百度搜索"""
        self.bai_du_page.load_url("https://www.baidu.com")
        self.bai_du_page.search()

    def test_china_railway(self):
        """12306日期"""
        self.china_railway.load_url("https://www.12306.cn/index/")
        time.sleep(5)  #
        self.china_railway.input_date("2021-01-01")

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()