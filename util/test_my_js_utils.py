from selenium import webdriver
from time import sleep

from base import Base
from js_demo import my_utils
from js_demo.js_utils import CssElement

class TestMyUtils(Base):
    # def setup(self):
    #     self.driver.get("https://www.baidu.com")
    #     # self.driver.get("https://www.12306.cn/index/")

    def test_input_clear_click(self):
        self.driver.get("https://www.baidu.com")
        # ele = CssElement(self.driver,'#kw')
        # ele.input('selenium')
        # sleep(3)
        # ele = CssElement(self.driver,'#su').click()
        # # ele.clear()
        my_utils.input('selenium',self.driver,'#kw')
        sleep(3)
        my_utils.clear(self.driver,'#kw')
        sleep(3)
        my_utils.input('appium', self.driver, '#kw')
        sleep(3)
        my_utils.click(self.driver,'#su')
        sleep(4)

    def test_remove_hight(self):
        self.driver.get("https://www.12306.cn/index/")
        ele = self.driver.find_element_by_css_selector("#train_date")
        my_utils.height_light(self.driver,"#train_date")
        sleep(2)
        # my_utils.remove_attribute("readonly",self.driver,"#train_date")
        my_utils.remove_attr(ele,"#train_date",self.driver)
        sleep(2)
        my_utils.input("2021-01-01",self.driver,"#train_date")
        sleep(2)


        my_utils.height_lig(self.driver,ele)
        sleep(5)

    def test_scroll(self):
        my_utils.input('selenium', self.driver, '#kw')
        sleep(3)
        my_utils.click(self.driver, '#su')
        sleep(4)
        wyb = self.driver.find_element_by_link_text("王一博 你要补一下妆")
        my_utils.scroll_to_element(self.driver,wyb)
        sleep(10)
        wyb.click()
        sleep(6)

# if __name__ == '__main__':
#     case = TestMyUtils()
#     case.test_input_clear()