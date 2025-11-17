import json
import os
import re
import subprocess
import requests
class BilibiliVideoDownloader:
    def __init__(self, url):
        self.url = url

    # 从html中提取音视频m4s链接
    def get_m4s_urls(self):
        # 发送初始HTML页面请求
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"}
        r = requests.get(self.url, headers=headers)
        html = r.text
        # 通过正则提取存储着视频链接的json
        pattern = re.compile(r'window\.__playinfo__=(.+?)</script>')
        json_str = pattern.findall(html)[0]
        data = json.loads(json_str)
        # 写入json查看data
        # with open('cache.json', 'w', encoding='utf-8') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)

        # 取出音视频m4s地址
        video_url = data['data']['dash']['video'][0]['backupUrl'][1]
        audio_url = data['data']['dash']['audio'][0]['backupUrl'][1]
        return video_url, audio_url

    # 分段的下载
    def download_by_range(self, url, name):
        # 通过name，先构建一个文件名
        name = 'cache.mp4' if 'v' in name else 'cache.mp3'
        h = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://www.bilibili.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'range': 'bytes=0-7941',
            'referer': 'https://www.bilibili.com/video/BV1yMpUzDEYa/?spm_id_from=333.788.player.switch&vd_source=8a215202e0c0f7127923c0c86ae40b57',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        }
        chunk = 1024 * 1024 * 3  # 单次请求range大小 3M
        # 获取url中range的总长
        r1 = requests.head(url, headers=h)
        # print(url)
        # print(r1.status_code)
        # print(r1.headers)
        total_range = int(r1.headers['Content-Range'].split('/')[1])
        for i in range(0, total_range, chunk):
            start = i
            end = min(i + chunk - 1, total_range - 1)
            print(f'正在下载{name}分片：{start} - {end}，总长：{total_range}')
            # 构建请求头
            h['range'] = f'bytes={start}-{end}'
            # 发送请求
            r = requests.get(url, headers=h)
            with open(name, 'ab') as f:
                f.write(r.content)

    # 合并
    def merge(self):
        subprocess.run([
            'ffmpeg',
            '-i', 'cache.mp4',
            '-i', 'cache.mp3',
            '-c:v', 'copy',
            '-c:a', 'aac',
            'output.mp4',
            '-y',
            '-loglevel', 'error',
        ])
        print('合并完成')
        os.remove('cache.mp4')
        os.remove('cache.mp3')

    def run(self):
        # 获取音视频m4s链接
        video_url, audio_url = self.get_m4s_urls()
        # 下载视频分段
        self.download_by_range(video_url, 'v')
        # 下载音频分段
        self.download_by_range(audio_url, 'a')
        # 合并
        self.merge()


if __name__ == '__main__':
    # 填视频播放页面的url
    url = "https://www.bilibili.com/video/BV1yMpUzDEYa/"
    downloader = BilibiliVideoDownloader(url)
    downloader.run()