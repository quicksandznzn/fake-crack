from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import os
import re
import zipfile


class ChromeDriver(object):
    """
        chrome driver
    """

    def __init__(
        self,
        privacy_proxy=None,
        proxy=None,
        headless=False,
        driver_name="mac_chromedriver_96.0.4664.45",
    ):

        self.up_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.driver_path = os.path.join(self.up_path, "chrome_driver", driver_name)
        self.options = Options()
        # common default settings
        self.options.add_argument("--dns-prefetch-disable")
        self.options.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug
        self.options.add_argument("disable-infobars")  # 隐藏'Chrome正在受到自动软件的控制'
        self.options.add_argument("--no-sandbox")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        if headless:
            self.options.add_argument("--headless")  # 增加无界面选项
        # 私密代理
        if privacy_proxy:
            self.options.add_extension(
                self.get_chrome_proxy_extension(proxy=privacy_proxy)
            )
        # 普通代理
        if proxy:
            self.options.add_argument("--proxy-server=%s" % proxy)

        self.driver = webdriver.Chrome(
            executable_path=self.driver_path, options=self.options
        )

    def get_chrome_proxy_extension(self, proxy):
        """
                获取一个Chrome代理扩展,里面配置有指定的代理(带用户名密码认证)
                proxy - 指定的代理,格式: username:password@ip:port
        """

        # Chrome代理模板插件(https://github.com/RobinDev/Selenium-Chrome-HTTP-Private-Proxy)
        chrome_proxy_helper_dir = os.path.join(self.up_path, "chrome-proxy-helper", "")
        custom_chrome_proxy_extensions_dir = os.path.join(
            self.up_path, "chrome-proxy-extensions", ""
        )
        m = re.compile("([^:]+):([^\@]+)\@([\d\.]+):(\d+)").search(proxy)
        if m:
            # 提取代理的各项参数
            username = m.groups()[0]
            password = m.groups()[1]
            ip = m.groups()[2]
            port = m.groups()[3]
            # 创建一个定制Chrome代理扩展(zip文件)
            if not os.path.exists(custom_chrome_proxy_extensions_dir):
                os.mkdir(custom_chrome_proxy_extensions_dir)
            extension_file_path = os.path.join(
                custom_chrome_proxy_extensions_dir,
                "{}.zip".format(proxy.replace(":", "_")),
            )
            if not os.path.exists(extension_file_path):
                # 扩展文件不存在，创建
                zf = zipfile.ZipFile(extension_file_path, mode="w")
                zf.write(
                    os.path.join(chrome_proxy_helper_dir, "manifest.json"),
                    "manifest.json",
                )
                # 替换模板中的代理参数
                background_content = open(
                    os.path.join(chrome_proxy_helper_dir, "background.js")
                ).read()
                background_content = background_content.replace("%proxy_host", ip)
                background_content = background_content.replace("%proxy_port", port)
                background_content = background_content.replace("%username", username)
                background_content = background_content.replace("%password", password)
                zf.writestr("background.js", background_content)
                zf.close()
            return extension_file_path
        else:
            raise Exception("Invalid proxy format. Should be username:password@ip:port")

    def get_cookies(self):
        """
            get cookies
        :return:
        """
        self.driver.refresh()
        cookies = self.driver.get_cookies()
        return cookies

    def trace_and_move(
        self, slider, x, y,
    ):
        """
            trace_and_move
        :param slider: 一般情况下是滑动按钮区域
        :param x: x
        :param y: y
        """

        ActionChains(self.driver).drag_and_drop_by_offset(
            slider, xoffset=(y - 56) / 2, yoffset=0
        ).perform()
        ActionChains(self.driver).release(slider).perform()
