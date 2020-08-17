import shelve
from selenium import webdriver

def test_wework_session():
    driver = webdriver.Firefox()
    driver.get('https://work.weixin.qq.com/wework_admin/frame')
    # # 将cookies使用shelve保持起来
    # db = shelve.open('cookies')# 有就打开一个文件，没有就新建
    # db['cookie'] = driver.get_cookies() # 将值赋值给cookies文件中的cookie（类似于键值对）

    # 需要用的时候打开
    db = shelve.open('cookies')
    cookies = db['cookie']
    for cookie in cookies:
        if 'expiry' in cookie.keys():
            cookie.pop('expiry')
        driver.add_cookie(cookie)
    driver.get('https://work.weixin.qq.com/wework_admin/frame')
    # 关闭shelve
    db.close()

if __name__ == '__main__':
    test_wework_session()
