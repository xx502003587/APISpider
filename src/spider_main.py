#coding=utf-8 
'''
工作流程：
1.从入口URL进行爬取
2.下载入口URL的源码进行解析——包括解析CSS文件
3.获得入口URL页面中所有符合条件的URL并加入容器中
4.将入口URL页面源码做指定修改后写入本地
5.如果容器不空，重复步骤1
'''
import url_manager, html_downloader, html_parser, html_outputer, xml_reader

class SpiderMain(object):
    def __init__(self, xml_file_name):
        #URL管理器
        self.urls = url_manager.UrlManager()
        #URL下载器
        self.downloader = html_downloader.HtmlDownloader()
        #URL解析器
        self.parser = html_parser.HtmlParser()
        #URL输出器
        self.outputer = html_outputer.HtmlOutputer()
        #XML解析器
        self.reader = xml_reader.xmlReader(xml_file_name)
    
    #爬虫调度程序
    def craw(self, root_url):
        #记录当前爬取的是第几个URL
        count = 1
        self.urls.add_new_url(root_url)
        
        #生成页面文件夹名称
        str_fold_name = root_url.split('/')
        fold_name = str_fold_name[len(str_fold_name)-1]
        #创建页面文件夹
        self.outputer.printFoldName(fold_name)
        
        #当集合中有带爬取URL时进行循环
        while self.urls.has_new_url():
            try:
                #1.当有新的URL时：获取一个新的URL
                new_url = self.urls.get_new_url()
                
                #输出当前正在爬取第几个URL
                print 'craw %d : %s' % (count, new_url)
                
                #2.启动下载器下载页面，页面源码存储在html_cont中
                html_cont = self.downloader.download(new_url)
              
                #3.调用解析器解析页面数据，得到新的URL列表和新的数据
                new_urls, new_title, new_html_cont = self.parser.parse(new_url, html_cont)   
                #new_urls, new_title = self.parser.parse(new_url, html_cont)   
                
                self.urls.add_new_urls(new_urls)
                #输出当前页面中有哪些URL
                #for i in new_urls:
                #    print i      
                print "Count------->" + str(self.urls.get_url_count())
                print
                       
                #4.写文件
                self.outputer.output_html(new_html_cont, new_title['title'])    
                #计数
                count = count + 1
                           
            except Exception as f:
                print 'crew failed: ', f

        print 'all finish'

if __name__=="__main__":
    obj_spider = SpiderMain("source.xml")
    
    #通过解析xml获取rootUrl字段
    root_url = obj_spider.reader.getAttrByTagName("rootUrl")
    #启动爬虫
    obj_spider.craw(root_url)