from ddddocr import DdddOcr
from playwright.sync_api import sync_playwright
import requests
import os
import random
import time

class movie_code():
    def __init__(self):
        self.page = None

    def download(self):
        img1 = self.page.locator(".geetest_bg")
        img1_url = img1.get_attribute("style").split('"')[1]
        response1 = requests.get(img1_url)
        with open("img1.jpg", "wb") as f:
            f.write(response1.content)
        img2 = self.page.locator(".geetest_slice_bg")
        img2_url = img2.get_attribute("style").split('"')[1]
        response2 = requests.get(img2_url)
        with open("img2.jpg", "wb") as f:
            f.write(response2.content)

    def generate_variable_track(self,total_distance): #AI生成变速函数
        """
        生成变速轨迹
        参数:
        - total_distance: 总移动距离
        返回:
        - 轨迹列表，每个元素是每一步的移动距离
        """
        track = []
        current = 0

        # 轨迹分为三个阶段：加速、匀速、减速
        while current < total_distance:
            remaining = total_distance - current

            # 加速阶段 (前30%)
            if current < total_distance * 0.3:
                step = random.uniform(2, 5)
            # 减速阶段 (后30%)
            elif current > total_distance * 0.7:
                step = random.uniform(1, 3)
            # 匀速阶段 (中间40%)
            else:
                step = random.uniform(3, 6)
            # 确保不会超过总距离
            if current + step > total_distance:
                step = remaining

            track.append(step)
            current += step

        return track


    def human_like_drag(self,page, start_x, start_y, target_x, target_y=None):
        """
        AI生成变速函数
        模拟人类行为的滑块拖动

        参数:
        - page: Playwright页面对象
        - start_x, start_y: 起始坐标
        - target_x, target_y: 目标坐标 (如果target_y为None，则使用start_y)
        - 返回: 无
        """
        if target_y is None:
            target_y = start_y

        # 计算总距离
        total_distance = target_x - start_x

        # 生成变速轨迹
        track = self.generate_variable_track(total_distance)

        # 执行拖动
        current_x = start_x
        current_y = start_y

        for step in track:
            # 添加微小随机延迟
            time.sleep(random.uniform(0.01, 0.03))

            # 计算下一步位置
            current_x += step
            # 添加微小垂直抖动
            current_y = start_y + random.uniform(-1, 1)

            # 移动鼠标
            page.mouse.move(current_x, current_y)

        # 确保最终位置准确
        page.mouse.move(target_x, target_y)



    def ocr_img(self): #识别图片
        img = self.page.locator('#captcha > div.geetest_captcha_e3cad411.geetest_captcha.geetest_float.geetest_customTheme.geetest_boxShow.geetest_freeze_wait > div.geetest_holder_e3cad411.geetest_holder > div.geetest_box_wrap_e3cad411.geetest_box_wrap > div.geetest_box_e3cad411.geetest_box > div.geetest_container_e3cad411.geetest_container > div > div > div.geetest_window_e3cad411.geetest_window > div.geetest_bg_e3cad411.geetest_bg')
        ocr = DdddOcr(show_ad=False)
        #得到两张图片
        self.download()
        #获取坐标
        with open("img1.jpg", "rb") as f:
            img_byts1 = f.read()
        with open("img2.jpg", "rb") as f:
            img_byts2 = f.read()
        res = ocr.slide_match(img_byts2,img_byts1,simple_target= True)['target'][0]
        os.remove("img1.jpg")
        os.remove("img2.jpg")
        return res

    def movie(self, int_x):
        # 模拟鼠标拖动
        botton = self.page.locator('.geetest_arrow')
        box = botton.bounding_box()
        slider_x = box['x'] + box['width'] / 2
        slider_y = box['y'] + box['height'] / 2

        self.page.mouse.move(slider_x, slider_y)
        self.page.mouse.down()

        self.human_like_drag(self.page, slider_x, slider_y, slider_x + int_x)

        self.page.mouse.up()

    def login(self):
        #进入验证环节
        self.page.click("#gt-showZh-mobile > div > section > div > div > div.tab-left > div.base-container > div.type-config > div.tab-item.tab-item-1")
        self.page.wait_for_timeout(1000)
        self.page.click(".geetest_btn_click")
        self.page.wait_for_timeout(4000)
        #识别图片，获取坐标
        int_x = self.ocr_img()
        #模拟鼠标拖动
        self.movie(int_x)


    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch( headless=False)
            context = browser.new_context()
            self.page = context.new_page()
            self.page.set_viewport_size({"width":1200,"height":900})
            self.page.goto("https://www.geetest.com/adaptive-captcha",wait_until="load")
            self.page.wait_for_timeout(1500)
            self.login()
            self.page.wait_for_timeout(2000)

if __name__ == '__main__':
    movie = movie_code()
    for i in range(5):
        print(f"第{i+1}次测试")
        try:
            movie.run()
            print("测试成功")
        except:
            print("测试失败")
        print("即将进入下次测试")
        time.sleep(5)
