#coding=utf-8 

import urllib2


class HtmlDownloader(object):
    
    #下载HTML文件
    def download(self, url):
        if url is None:
            return None
        
        response = urllib2.urlopen(url)       
        
        if response.getcode() != 200:
            print "path failed"
            return None
        
        return response.read()
        
    #下载CSS文件    
    def download_css(self, css_url):
        if css_url is None:
            return None
        
        response = urllib2.urlopen(css_url)
        if response.getcode() != 200:
            print "path failed"
            return None
        
        return response.read()



