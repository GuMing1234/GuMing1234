from bs4 import BeautifulSoup
import requests
import lxml
import os
import time
class Note_spider():
    def __init__(self,url):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"}
        self.url = url
        self.soup = None
        self.hrefs = None
    def get_html(self):
        response = requests.get(self.url,headers=self.headers)
        self.soup = BeautifulSoup(response.text,"lxml")
        self.hrefs = self.soup.select(".listmain a")
    def get_name(self):
        name = self.soup.select(".info h1")[0].text
        os.mkdir(name)
        return name

    def get_content(self,name):
        for href in self.hrefs:
            if(href["href"]=="javascript:dd_show()"):
                continue
            url2="https://www.2b402cea57.sbs"+href["href"]
            response2 = requests.get(url2,headers=self.headers)
            soup2 = BeautifulSoup(response2.text,"lxml")
            name2 = soup2.select("div.content > h1")[0].text
            content = soup2.select("#chaptercontent")[0].get_text("\n",strip=True)
            with open(f"{name}/{name2}.txt", "w", encoding="utf-8") as f:
                f.write(content)
                print(f"{name2},保存成功")
                time.sleep(1)
    def run(self):
        self.get_html()
        name = self.get_name()
        self.get_content(name)
a=Note_spider("https://www.bqgde.de/book/61808/")
a.run()
