import requests
import json
import time
import re
from jsonpath import jsonpath
import os
import subprocess
import shutil
from urllib.parse import urljoin

class AcFun:
    def __init__(self, url):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }
        self.url = url

    def get_list(self):
        os.makedirs("temp",exist_ok=True)

    def get_m3u8(self):
        response = requests.get(self.url, headers=self.headers)
        original_data = re.findall(r"window\.pageInfo = window\.videoInfo = (.+?);", response.text)[0]
        json_data = json.loads(original_data)
        new_json_data = jsonpath(json_data,"$..ksPlayJson")[0]
        new_json_data = json.loads(new_json_data)
        m3u8_url = jsonpath(new_json_data,"$..representation")[0][0]["url"]
        return m3u8_url

    def get_ts(self, m3u8_url):

        m3u8=requests.get(m3u8_url, headers=self.headers).text
        lists = m3u8.splitlines()
        ts_urls = []
        for i in lists:
            if "#" not in i:
                ts_urls.append(i)
        return ts_urls
    def download_ts(self, ts_urls,m3u8_url):
        lens =len(ts_urls)
        for i,ts_url in enumerate(ts_urls,1):
            if not ts_url.startswith("http"):
                ts_url = urljoin(m3u8_url, ts_url)
            ts_data = requests.get(ts_url, headers=self.headers)
            with open(f"temp/{i}.ts","wb") as f :
                f.write(ts_data.content)
                print(f"已下载{i/lens * 100:.2f}%")
            with open(f"temp/file.txt","a",encoding="utf-8") as f:
                f.write(f"file '{i}.ts'\n")
            time.sleep(0.5)

    def merge_ts(self):
        print("视频合并中...")
        subprocess.run([
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', 'temp/file.txt',
            '-c', 'copy',
            'output.mp4',
            '-loglevel', 'error',
            '-y',
        ])
        shutil.rmtree("temp")
        print("视频已下载完成！")

    def run(self):
        self.get_list()
        m3u8_url = self.get_m3u8()
        ts_urls = self.get_ts(m3u8_url)
        self.download_ts(ts_urls,m3u8_url)
        self.merge_ts()




test = AcFun("https://www.acfun.cn/v/ac47863239")
test.run()
