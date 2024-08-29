from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor as thrd
import re, time, json

app = Flask("asynchronous-selenium-replit-reloader")

waktuItu = int(time.time())

replUrl_1 = "url1".split("#") # url repl saat ini
replUrl_2 = "url2".split("#") # url repl yang ingin dibikin 24/7 (wajib satu akun dengan url repl saat ini / replUrl_1)

replUrl_1 = "#".join(part for part in (replUrl_1 if len(replUrl_1) == 1 else replUrl_1[:-1])) + "#fast.txt"
replUrl_2 = "#".join(part for part in (replUrl_2 if len(replUrl_2) == 1 else replUrl_2[:-1])) + "#fast.txt"

def cookieParser():
    cookies = json.loads(open("cookies.txt", "r").read())
    ubahSameSite = {
        "no_restriction": "None",
        "unspecified": "Lax"
    }
    for cookie in range(len(cookies)):
        tempValue = cookies[cookie]["sameSite"]
        cookies[cookie]["sameSite"] = ubahSameSite[tempValue] if tempValue in ubahSameSite else tempValue.capitalize()
    return cookies

class Worker:
    def __init__(self, options, cookies, replUrl, image):
        self.driver = webdriver.Chrome(options=options)
        self.cookies = cookies
        self.replUrl = replUrl
        self.image = image
        self.firstLoop = True
        self.waitUntil = 15
        self.befTime = None
        self.sourceStop = None
        self.sourceRun = None

    def backgroundJob(self):
        self.driver.get("https://replit.com")
        self.driver.delete_all_cookies()
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)
        while True:
            self.driver.get(self.replUrl)
            self.befTime = int(time.time())
            while True:
                self.sourceStop = re.search(">Stop<", self.driver.page_source)
                self.sourceRun = re.search(">Run<", self.driver.page_source)
                if self.sourceStop or self.sourceRun:
                    break
                if int(time.time()) - self.befTime >= self.waitUntil:
                    break
            self.driver.save_screenshot(self.image)
            if self.firstLoop:
                self.firstLoop = False
                self.waitUntil = 1

@app.route("/", methods=["GET"])
def index():
    return f"{(int(time.time()) - waktuItu) // 60} menit telah dilalui, repl-mu masih tetap aktif 🥰"

if __name__=="__main__":
    cookies = cookieParser()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")
    Browser_1 = Worker(options, cookies, replUrl_1, "image_1.png")
    Browser_2 = Worker(options, cookies, replUrl_2, "image_2.png")
    with thrd(max_workers=3) as runner:
        runner.submit(app.run, host="0.0.0.0", port=5000)
        runner.submit(Browser_1.backgroundJob)
        runner.submit(Browser_2.backgroundJob)
