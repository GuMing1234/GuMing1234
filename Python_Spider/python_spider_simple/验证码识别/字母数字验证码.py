from ddddocr import DdddOcr
from playwright.sync_api import sync_playwright
import os

class ocr_code():
    def __init__(self):
        self.ddddocr = DdddOcr()

    def v_code(self):
        img = self.page.locator('#app > div.login-page > div.login-container.pt-1 > div.login-core.mt-50 > div.login-core-container > div.form-box > form > div:nth-child(4) > div > div:nth-child(3) > img')
        img_bytes = img.screenshot(path = "img.jpg")
        ocr = DdddOcr(show_ad=False)
        text = ocr.classification(img_bytes)
        return text

    def login(self):
        self.page.fill('#app > div.login-page > div.login-container.pt-1 > div.login-core.mt-50 > div.login-core-container > div.form-box > form > div:nth-child(1) > div > div > input',"18835998788")
        self.page.fill('#app > div.login-page > div.login-container.pt-1 > div.login-core.mt-50 > div.login-core-container > div.form-box > form > div:nth-child(2) > div > div > input',"song13703594591")
        #获取验证码
        verfication_code = self.v_code()
        self.page.fill("#app > div.login-page > div.login-container.pt-1 > div.login-core.mt-50 > div.login-core-container > div.form-box > form > div:nth-child(4) > div > div:nth-child(1) > div > div > div.el-input.el-input--prefix.el-input--suffix > input",verfication_code)
        self.page.click("#app > div.login-page > div.login-container.pt-1 > div.login-core.mt-50 > div.login-core-container > div.form-box > form > div.el-form-item.mt-15 > div > button > span")
        os.remove("img.jpg") #用完删掉图片避免占用内存

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=False)
            context = browser.new_context()
            self.page = context.new_page()
            self.page.set_viewport_size({"width":700,"height":500})
            self.page.goto("https://i.kol.cn/login")
            self.page.wait_for_timeout(1500)
            #登录
            self.login()
            self.page.wait_for_timeout(50000)

if __name__ == '__main__':
    ocr = ocr_code()
    ocr.run()