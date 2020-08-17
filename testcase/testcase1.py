from time import sleep

from selenium import webdriver

from util.my_utils import get_element_location


def testcase1():
    driver = webdriver.Firefox()
    driver.get('http://localhost:8080/jpress/user/register')


    sleep(3)
    captch = driver.find_element_by_id('captchaimg')
    print("captch")
    loc = get_element_location(captch)

    print(loc)
    sleep(3)
    driver.quit()