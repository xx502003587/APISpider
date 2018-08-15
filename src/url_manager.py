#coding=utf-8 


class UrlManager(object):
    def __init__(self):
        self.new_urls = list()
        self.old_urls = list()
    
    #向管理器中添加一个新的URL
    def add_new_url(self, url):
        if url is None:
            return
        
        #如果当前URL未被爬取  则添加进容器中
        if url not in self.new_urls and url not in self.old_urls:
            print url
            self.new_urls.append(url)
            
        
    #向管理器中添加批量URL
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:  
            return 
        
        for url in urls:  
            self.add_new_url(url)
            
            
    #判断管理器中是否还有待爬取的URL
    def has_new_url(self):
        return len(self.new_urls) != 0

    #从管理器中取出一个新的URL
    def get_new_url(self):
        #先获取一个URL
        new_url = self.new_urls.pop(0)
        #放入旧的URL列表
        self.old_urls.append(new_url)
        
        return new_url

    #获得待爬取URL个数
    def get_url_count(self):
        return len(self.new_urls)
    