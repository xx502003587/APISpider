#coding=utf-8 

import os
from baike_spider import xml_reader

class HtmlOutputer(object):
    def __init__(self):
        self.datas = []
        #指定路径（改）
        self.reader = xml_reader.xmlReader("source.xml")
        #通过解析xml获取资源存放路径srcPath
        srcName = self.reader.getAttrByTagName("srcPath")
        #设置文件存放路径（改）
        self.path = os.getcwd() + "\\resource\\" + srcName + "\\"
        
        if not os.path.isdir(self.path):  
            os.makedirs(self.path)        # 创建文件夹
    
    #输出html文件
    def output_html(self, text, title):
        
        savepath = self.path + title + ".html"
              
        with open(savepath, 'wb') as code:  
            code.write(text)

    #输出css文件
    def output_css(self, foldName, textPath, content):
        
        savepath = self.path + foldName
        
        if not os.path.isdir(savepath):  
            os.makedirs(savepath)        # 创建文件夹
              
        textPath = self.path + textPath
        with open(textPath, 'wb') as code:  
            code.write(content)

    #输出文件夹名称
    def printFoldName(self, name):
        self.path = self.path + name + "\\"
        
        if not os.path.isdir(self.path):  
            os.makedirs(self.path)        # 创建文件夹
    