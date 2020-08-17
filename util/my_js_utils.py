from selenium import webdriver
from time import sleep,strftime,localtime,time
import os
def _set_index(index=None):
    """
    index判断赋值
    :param index:
    :return:
    """
    if index is None:
        index = 0
    else:
        index = index
    return index
def clear(driver: webdriver, css,index=None, describe=None):
    """
    用途：用来清除输入框的内容
    :param driver: webdriver
    :param css: css选择器
    :param index: 列表的下标
    :param describe: 描述信息
    :return:
    """

    js = """var elm = document.querySelectorAll("{css}")[{index}];
                        elm.style.border="2px solid red";
                        elm.value = "";""".format(css=css, index=_set_index(index))
    driver.execute_script(js)


def input(value,driver: webdriver, css,index=None, describe=None):
    """
    用途：输入框中输入内容
    :param self:
    :param value:待输入的数据
    :param driver: webdriver
    :param css: css选择器
    :param index: 列表的下标
    :param describe: 描述信息
    :return:
    """
    js = """var elm = document.querySelectorAll("{css}")[{index}];
                elm.style.border="2px solid red";
                elm.value = "{value}";""".format(css=css, index=_set_index(index), value=value)
    driver.execute_script(js)


def click(driver: webdriver, css,index=None, describe=None):
    """
    用途：由于web自动化的最大问题就是稳定性比较差，有些时候使用selenium无法点击元素，因此我们可以使用JS实现元素的点击操作
    :param self:
    :param driver: webdriver
    :param css: css选择器
    :param index: 列表的下标
    :param describe: 描述信息
    :return:
    """
    js = """var elm = document.querySelectorAll("{css}")[{index}];
               elm.style.border="2px solid red";
               elm.click();""".format(css=css, index=_set_index(index))
    driver.execute_script(js)


def remove_attribute(attribute,driver: webdriver, css,index=None, describe=None):
    """
    用途：以下方法可以删除元素的任何属性，主要用来移除时间控件的readonly属性
    :param attribute:元素的某个属性，比如readonly，value，name等
    :param driver: webdriver
    :param css: css选择器
    :param index: 列表的下标
    :param describe: 描述信息
    :return:
    """
    # _index_(index)
    js = """
    var elm = document.querySelectorAll("{css}")[{index}];
        elm.removeAttribute("{attr}");
    """.format(css=css, index=_set_index(index), attr=attribute)
    driver.execute_script(js)


def remove_attr(element, attribute,driver: webdriver):
    """
    用途：以下方法可以删除元素的任何属性
    :param element: 需要被删除属性的控件
    :param attribute: 需要删除的属性
    :param driver: webdriver
    :return:
    """
    js = """
    arguments[0].removeAttribute("{attr}");
    """.format(attr=attribute)
    driver.execute_script(js, element)


def scroll_to_xy(driver: webdriver,x, y):
    '''
    用途：通过制定xy坐标来滑动web页面
    :param driver: webdriver
    :param x:屏幕向右移动的距离
    :param y:屏幕向下移动的距离
    :return:

    1、滚动到文档中的某个坐标
    window.scrollTo(x-coord,y-coord )
    window.scrollTo(options)
        ·x-coord 是文档中的横轴坐标。
        ·y-coord 是文档中的纵轴坐标。
        ·options 是一个包含三个属性的对象:
            ·top 等同于  y-coord
            ·left 等同于  x-coord
            ·behavior  类型String,表示滚动行为,支持参数 smooth(平滑滚动),instant(瞬间滚动),默认值auto,实测效果等同于instant
    例子：
        window.scrollTo( 0, 1000 );

        // 设置滚动行为改为平滑的滚动
        window.scrollTo({
            top: 1000,
            behavior: "smooth"
        });
    '''
    js = """
    window.scrollTo("{}", "{}")
    """.format(x, y)
    driver.execute_script(js)

# TODO：没整明白到底怎么个滑动法
def window_scroll(driver: webdriver,element, x, y):
    """
    用途：指定元素移动的某位置
    :param driver: webdriver
    :param element: 指定元素
    :param x:屏幕向右移动的距离
    :param y:屏幕向下移动的距离
    :return:
    """
    js = """
    arguments[0].scrollTo("{}", "{}")
    """.format(x, y)
    driver.execute_script(js, element)

def scroll_to_element(driver: webdriver,element):
    """
    用途：滚动屏幕使得元素上下、左右居中
    :param driver:
    :param element:
    :return:
    """
    js = "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});"
    driver.execute_script(js, element)


def height_light(driver: webdriver, css,index=0):
    """
    用途：方便用户查看当前操作的是哪个页面元素，也方便测试人员定位问题
    :param driver: webdriver
    :param css: css选择器
    :param index: 列表的下标
    :return:
    """
    js = """
    var element = document.querySelectorAll("{css}")[{index}];
        element.style.border="4px solid red";
    """.format(css=css, index=index)
    driver.execute_script(js)


def height_lig(driver: webdriver,element):
    """
    用途：指定元素高亮
    :param driver: webdriver
    :param element: 需要高亮的元素
    :return:
    """
    js = """
    arguments[0].style.border="2px solid red";
    """
    driver.execute_script(js, element)


def save_screenshot(driver: webdriver,sub_filename,element,describe=None):
    """
    用途：对当前屏幕截图并保存到当前路径，同时标记被操作的元素为高亮，图片文件名格式为：当前时间+sub_filename.png
    :param driver: webdriver
    :param sub_filename: 文件的部分名称，为了区分建议用selector命名
    :param element: 需要被高亮的元素
    :param describe: 方法的描述，同时也作为png图片文件名的一部分
    :return:
    """
    name = os.path.abspath('screenshot')+'/'
    # name = "C:/Users/Administrator/PycharmProjects/haige_selenium/screenshot/"
    st = strftime("%Y-%m-%d-%H-%M-%S",localtime(time()))
    file_name = name+st+'-'+sub_filename+describe+".png"
    height_lig(driver,element)
    driver.save_screenshot(file_name);