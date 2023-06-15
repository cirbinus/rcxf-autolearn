import requests        # 请求并下载相应的msedgedriver版本
import zipfile        # 用于解压下载文件
import os        # 检查目录下的文件
import re        # 对信息进行正则匹配
import xml.dom.minidom        # 处理包含浏览器版本信息的xml文件
from selenium.common.exceptions import *
from selenium import webdriver
from selenium.webdriver.edge.options import Options


def unzip(file_dir, out_dir):
    zf = zipfile.ZipFile(file_dir)    # 实例化压缩文件
    try:
        zf.extract('msedgedriver.exe', path=out_dir)    # 解压文件
    except RuntimeError as e:
        print(e)
    zf.close()


class UpdateEdge:
 
    def __init__(self, src_dir):
        self.src_dir = src_dir
 
    def update_edge(self):
        if os.path.isfile(self.src_dir+'msedgedriver.exe'):     # 查看是否有msedgedriver.exe文件
            pass
        else:
            print('正在安装/更新驱动...\n')
            dom = xml.dom.minidom.parse(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge'
                                        r'.VisualElementsManifest.xml')     # 读取edge文件夹下面的xml文件(包含版本信息)
            dom_ele = dom.documentElement
            ve = dom_ele.getElementsByTagName('VisualElements')
            ve_text = ve[0].toxml()     # 包含版本号的字符串文本
            rematch = re.match(r'(.*)\"(.*)\\VisualElements\\Logo.png', ve_text)
            edge_version = rematch.group(2)     # 匹配得到版本号
            url = 'https://msedgedriver.azureedge.net/'+edge_version+'/edgedriver_win64.zip'
            response = requests.get(url=url)    # 请求edgedriver下载链接
            file_dir = self.src_dir+edge_version+'edgedriver_win64.zip'
            print('正在下载驱动...\n')
            open(file_dir, 'wb').write(response.content)    # 下载edgedriver压缩包
            print('正在解压驱动...\n')
            unzip(file_dir, self.src_dir)   # 在下载目录下解压edgedriver压缩包
            if os.path.isfile(file_dir):
                os.remove(file_dir)
            else:
                pass
        try:
            options = Options()
            options.add_argument('headless')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--log-level=3')
            webdriver.Edge(options=options)
        except SessionNotCreatedException as msg:
            print('正在重新匹配驱动...\n')
            reg = re.search("(.*)Current browser version is (.*) with", str(msg))    # 识别并匹配Exception信息中出现的版本号
            edge_version = reg.group(2)    # 获得版本号
            url = 'https://msedgedriver.azureedge.net/'+edge_version+'/edgedriver_win64.zip'
            response = requests.get(url=url)
            file_dir = self.src_dir+edge_version+'.zip'
            print('正在下载驱动...\n')
            open(file_dir, 'wb').write(response.content)    # 下载压缩文件
            print('正在解压驱动...\n')
            unzip(file_dir, self.src_dir)    # 解压文件
            if os.path.isfile(file_dir):
                os.remove(file_dir)    # 将多余的压缩文件删除
            else:
                pass
        print("驱动安装完成!!!\n")
        pass
 
 
# if __name__ == '__main__':
#     os.chdir(os.path.dirname(__file__))
#     source_dir = os.path.dirname(__file__)
#     up = UpdateEdge(source_dir)
#     up.update_edge()