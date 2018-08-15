#coding=utf-8 

import xml.etree.ElementTree as ET

class xmlReader(object):

    def __init__(self, xml_name):
        self.tree = ET.parse(xml_name)
        self.tRoot = self.tree.getroot()
    
    #通过标签名获取单个属性
    def getAttrByTagName(self, tag_name):
        content = self.tRoot.find(tag_name).text
        return content
    
    #通过标签名获得多个属性并返回字典
    def getAttrsDict(self, tag_name):
        content = self.tRoot.find(tag_name)
        dict = {}
        for child in content:
            dict[child.tag] = child.text
            
        return dict
    
    def getAttrsList(self, tag_name):
        content = self.tRoot.findall(tag_name)
        keywordList = list()
        for child in content:
            if child.attrib['required'] == "required":
                for child2 in child:
                    #print child2.text
                    keywordList.append(child2.text)
        
        return keywordList