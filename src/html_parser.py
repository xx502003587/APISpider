#coding=utf-8
from bs4 import BeautifulSoup
import re
import urlparse
import os
from baike_spider import html_downloader, html_outputer, xml_reader

class HtmlParser(object):
    def __init__(self):
        self.reader = xml_reader.xmlReader("source.xml")
        #通过解析xml获取资源存放路径srcPath
        srcName = self.reader.getAttrByTagName("srcPath")
        #设置文件存放路径（改）
        self.path = os.getcwd() + "\\resource\\" + srcName + "\\"
        #URL下载器
        self.downloader = html_downloader.HtmlDownloader()
        #URL输出器
        self.outputer = html_outputer.HtmlOutputer()
        #存放css文件路径的list
        self.css_url = list()

    #获取当前页面下的所有URL
    def _get_new_urls(self, page_url, soup):
        new_urls = list()

        #通过解析xml获取需爬取页面块
        tmp_module = self.reader.getAttrsDict("htmlModule")
        #指定需要爬取的页面块(改)
        new_div = soup.find(tmp_module['tag'], id=tmp_module['id'])

        #通过解析xml获得URL的正则表达式
        links = new_div.find_all('a', href = re.compile(eval(self.reader.getAttrByTagName('urlFormat'))))

        #通过解析xml获得URL排除的关键字信息
        keywordList = self.reader.getAttrsList("keywordScan")

        for link in links:
            result = True
            #print "check++" + link['href']
            for i in range(0, len(keywordList)):
                test_keyword = re.search(keywordList[i], str(link['href']))
            #    print "----check keyword : " + keywordList[i] + "->>" + str(test_keyword)
                result = result and (not test_keyword)
            #    print "----check answer : " + str(result)
                if result == False:
                    break

            if result == True:
                new_url = link['href']
                new_full_url = urlparse.urljoin(page_url, new_url)
                new_urls.append(new_full_url)

        return new_urls

    #获取页面中的 h1 标签的 text 属性作为html文件的名称(改)
    def _get_new_data(self, page_url, soup):
        res_data = {}
        #url
        res_data['url'] = page_url

        summary_node = soup.find('h1')
        res_data['title'] = summary_node.get_text()
        return res_data


    #获取当前URL源码的所有css文件路径
    def _get_css_data(self, page_url, html_cont, soup):
        #获取存放css的文件夹名称，即当前页面的h1属性值
        fold_name = soup.find('h1').get_text()

        #查找所有的css语句
        css_path = soup.find_all('link', type="text/css")

        #css_path下存放的是页面所有css
        for tmp in css_path:
            #拿到css路径
            css_str = tmp['href'] # tmp['href']是源代码中的css的href路径

            #将不完整的CSS路径名补充完整（改）
            if css_str[0] == '/' :
                css_str = self.reader.getAttrByTagName("cssNamePath") + css_str

            #解析css文件名称
            css_name_string = css_str.split('/')

            #组成css文件名称
            css_file_name = css_name_string[len(css_name_string) - 1]

            #print new_css_path    # Publishing/css/mdn.07c1cb24024c.css

            #如果当前CSS文件未被爬取过，则爬取
            if self.judge_css(css_str) == True:
                #下载css文件内容
                print "下载css文件内容-----"
                print  css_str
                css_content = self.downloader.download_css(css_str)
                foldName = fold_name + "\\css"
                new_css_path = foldName + "\\" + css_file_name
                self.outputer.output_css(foldName, new_css_path, css_content)

            #替换源文件中的css路径（改）
            #将源文件中的css路径由绝对路径改为相对路径且放于当前目录的css文件夹中，即css/xxxx.css
            tmpPath = "css/" + css_file_name
            html_cont = html_cont.replace(tmp['href'].encode('utf-8'), tmpPath.encode('utf-8'))

        return html_cont


    #解析当前页面URL
    def parse(self, page_url, html_cont):
        #如果页面URL为空则返回
        if page_url is None or html_cont is None:
            return

        #获取页面的bs对象
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')

        #获取当前URL下的所有URL
        new_urls = self._get_new_urls(page_url, soup)

        #获取当前URL的h1属性中的text作为页面的标题
        new_data = self._get_new_data(page_url, soup)

        #获取当前URL源码的所有css文件路径
        new_html_cont = self._get_css_data(page_url, html_cont, soup)

        return new_urls, new_data, new_html_cont
        #return new_urls, new_data

    #判断当前CSS的URL是否已被爬取，若没有，则加入容器中
    def judge_css(self, tmp_css_url):
        if tmp_css_url not in self.css_url:
            self.css_url.append(tmp_css_url)
            return True
        else :
            return False
