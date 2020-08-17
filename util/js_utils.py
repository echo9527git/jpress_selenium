class CssElement(object):

    def __init__(self,driver, css, index=None, describe=None):
        '''

        :param css: css选择器
        :param index: 列表的下标
        :param describe: 描述信息
        '''
        self.css = css
        self.driver = driver
        if index is None:
            self.index = 0
        else:
            self.index = index
        self.desc = describe

    def __get__(self, instance, owner):
        if instance is None:
            return None
        global driver
        driver = instance.driver
        return self

    def clear(self):
       '''
       用途：用来清除输入框的内容
       :return:
       '''
       js = """var elm = document.querySelectorAll("{css}")[{index}];
                            elm.style.border="2px solid red";
                            elm.value = "";""".format(css=self.css, index=self.index)
       self.driver.execute_script(js)

    def input(self, value):
        '''
        用途：输入框中输入内容
        :param self:
        :param value:待输入的数据
        :return:
        '''
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.style.border="2px solid red";
                    elm.value = "{value}";""".format(css=self.css, index=self.index, value=value)
        self.driver.execute_script(js)

    def click(self):
        '''
        用途：由于web自动化的最大问题就是稳定性比较差，有些时候使用selenium无法点击元素，因此我们可以使用JS实现元素的点击操作
        :return:
        '''
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                   elm.style.border="2px solid red";
                   elm.click();""".format(css=self.css, index=self.index)
        self.driver.execute_script(js)

    def remove_attribute(self, attribute):
        '''
        用途：以下方法可以删除元素的任何属性，主要用来移除时间控件的readonly属性
        :param attribute:元素的某个属性，比如readonly，value，name等
        :return:
        '''
        js = """
        var elm = document.querySelectorAll("{css}")[{index}];
            elm.removeAttribute("{attr}");
        """.format(css=self.css, index=self.index, attr=attribute)
        self.driver.execute_script(js)

    def remove_attr(self,element, attribute):
        '''
        用途：以下方法可以删除元素的任何属性
        :param element: 需要被删除属性的控件
        :param attribute: 需要删除的属性
        :return:
        '''
        js = """
        arguments[0].removeAttribute("{attr}");
        """.format(attr=attribute)
        self.driver.execute_script(js, element)

    def scrollTo(self,x, y):
        '''
        用途：滑动web页面
        :param x:屏幕向右移动的距离
        :param y:屏幕向下移动的距离
        :return:
        '''
        js = """
        window.scrollTo("{}", "{}")
        """.format(x, y)
        self.driver.execute_script(js)

    def window_scroll(self,element, x, y):
        js = """
        arguments[0].scrollTo("{}", "{}")
        """.format(x, y)
        self.driver.execute_script(js, element)

    def height_light(self):
        '''
        用途：方便用户查看当前操作的是哪个页面元素，也方便测试人员定位问题
        :return:
        '''
        js = """
        var element = document.querySelectorAll("{css}")[{index}];
            element.style.border="2px solid red";
        """.format(css=self.css, index=self.index)
        self.driver.execute_script(js)

    def height_lig(self,element):
        js = """
        arguments[0].style.border="2px solid red";
        """
        driver.execute_script(js, element)


if __name__ == '__main__':
    pass