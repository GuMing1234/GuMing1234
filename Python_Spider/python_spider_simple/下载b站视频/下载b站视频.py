import re
import os
import time
import requests
import json
import subprocess
class download_bilibili_video():
    def __init__(self,url,name):
        self.name=name
        self.length1=0
        self.length2=0
        self.url=url
        self.headers={
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://www.bilibili.com',
    'priority': 'u=1, i',
    'referer': 'https://www.bilibili.com/video/BV1XmnhzVEby/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=47f23df979124805432636f780cc9684',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
    'sec-ch-ua-mobile': '?0',
    'range':'bytes=0-99',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
}
        self.cookies = {
    'buvid3': 'CAC74196-AF2D-DC5F-7D75-3BE784B60C5369103infoc',
    'b_nut': '1755753969',
    '_uuid': 'F92AB7BE-EEFC-4E6D-89CC-CDFACB910163669829infoc',
    'buvid_fp': '5926ee6841db94793d33acc6e4e5c9f0',
    'rpdid': "|(k|kYm||RmJ0J'u~ll~lJm~|",
    'buvid4': 'F037168B-5710-4585-336F-2B996370EA1F70283-025082113-Q/JmEATAD/6zxQoRtL208g%3D%3D',
    'enable_web_push': 'DISABLE',
    'DedeUserID': '414870071',
    'DedeUserID__ckMd5': 'd4151ed73a476984',
    'theme-tip-show': 'SHOWED',
    'theme-avatar-tip-show': 'SHOWED',
    'CURRENT_QUALITY': '80',
    'home_feed_column': '4',
    'browser_resolution': '1272-721',
    'b_lsid': '3E104BDC1_19A8C76A011',
    'bsource': 'search_bing',
    'bmg_af_switch': '1',
    'bmg_src_def_domain': 'i1.hdslb.com',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjM1NTIzNzYsImlhdCI6MTc2MzI5MzExNiwicGx0IjotMX0.z1MWHLXSCiYYMww_L7edLkR30HE-F5IjU5VRrDEFkKg',
    'bili_ticket_expires': '1763552316',
    'SESSDATA': 'c8942342%2C1778845176%2Cf6a17%2Ab2CjC4lXIIu-IZ_WK8FQV3RB4JDepMo1GHYUTmbjvBmzA21BdlrLvGIpkmErd3h06NztgSVnl6ajVwVU5DLXVqTHBMZDhDcTZ4TXRrUzM5d0xaRjNBcXFUR1g0RGlrME9CMHViampmeE5jcDZCR0N6U0pTaTZobllwRENjQ1ZDUm50aWlEZ1hyajVnIIEC',
    'bili_jct': '0760ce682a5771f14db56025a698159f',
    'CURRENT_FNVAL': '4048',
    '_qimei_uuid42': '19b10132a301009392b99841434ddba9db0d2bb497',
    '_qimei_fingerprint': '783ffd6317414455af78a2872b55a07f',
    '_qimei_i_3': '40c05bd4905d038d9596f73959d277e6f2bcf6f412090780b6db2051709a293863633f943c89e29b9497',
    'sid': '6p1dzpd3',
    'bp_t_offset_414870071': '1135826186149036032',
}
        self.h={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"}
    def get_json(self):
        response = requests.get(self.url,headers=self.h,cookies=self.cookies)
        jsons=re.findall("__playinfo__=(.+?)</script>",response.text)[0]
        json_data=json.loads(jsons)
        return json_data

    def get_video_url(self,json_data):
        video_url=json_data["data"]["dash"]["video"][0]["baseUrl"]
        audio_url=json_data["data"]["dash"]["audio"][0]["baseUrl"]
        return video_url,audio_url

    def get_video_length(self,video_url,audio_url):
        response1 = requests.get(video_url,headers=self.headers)
        response2 = requests.get(audio_url, headers=self.headers)
        video_length=response1.headers["Content-Range"]
        video_length=int(video_length.split("/")[1])
        audio_length=response2.headers["Content-Range"]
        audio_length=int(audio_length.split("/")[1])
        self.length1=video_length
        self.length2=audio_length

    def download_video(self,video_url,audio_url):
        lens=1024 * 1024 * 10
        for i in range(0,self.length1,lens):
            start=i
            end=min(i+lens-1,self.length1-1)
            self.headers["range"]=f"bytes={start}-{end}"
            video_data=requests.get(video_url,headers=self.headers)
            with open("video.mp4","ab") as f:
                f.write(video_data.content)
            print(f"视频已下载{(end / (self.length1 - 1) * 100):.2f}%")
            time.sleep(0.2)
        for i in range(0,self.length2,lens):
            start=i
            end=min(i+lens-1,self.length2-1)
            self.headers["range"]=f"bytes={start}-{end}"
            audio_data=requests.get(audio_url,headers=self.headers)
            with open("audio.mp3","ab") as f:
                f.write(audio_data.content)
            print(f"音频已下载{(end / (self.length2 - 1) * 100):.2f}%")
            time.sleep(0.2)


    def add_video_audio(self):
        print("正在合并视频和音频...")
        subprocess.run([
            'ffmpeg',
            '-i', 'video.mp4',
            '-i', 'audio.mp3',
            '-c:v', 'copy',
            '-c:a', 'aac',
            f'{self.name}.mp4',
            '-loglevel','error',
            '-y',
        ])
        print("全部下载成功！")
        os.remove("video.mp4")
        os.remove("audio.mp3")

    def run(self):
        json_data=self.get_json()
        video_url,audio_url=self.get_video_url(json_data)
        self.get_video_length(video_url,audio_url)
        self.download_video(video_url,audio_url)
        self.add_video_audio()
if __name__ == '__main__':
    url=input("请输入视频的url:")
    name=input("请输入视频保存名称:")
    download = download_bilibili_video(url, name)
    res=requests.get(url,headers=download.h,cookies=download.cookies)
    if res.status_code in [200,206]:
        print("正在准备下载，请稍等...")
        download.run()
    else :
        print("cookies失效或者其他错误")
