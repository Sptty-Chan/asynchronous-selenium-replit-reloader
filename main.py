from flask import Flask
from flask_executor import Executor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor as thrd
import re, time, json

app = Flask("asynchronous-selenium-replit-reloader")
executor = Executor(app)

worker = False
waktuItu = int(time.time())

replUrl_1 = "" #url repl saat ini
replUrl_2 = "" #url repl yang ingin dibikin 24/7 (wajib satu akun dengan url repl saat ini / replUrl_1)

def cookieParser():
    cookies = json.loads(open("cookies.txt", "r").read())
    for cookie in range(len(cookies)):
        if cookies[cookie]["sameSite"] == "no_restriction":
            cookies[cookie]["sameSite"] = "None"
        elif cookies[cookie]["sameSite"] == "unspecified":
            cookies[cookie]["sameSite"] = "Lax"
        else:
            cookies[cookie]["sameSite"] = cookies[cookie]["sameSite"].replace(cookies[cookie]["sameSite"][0], cookies[cookie]["sameSite"][0].upper())
    return cookies

def backgroundWorker():
    global worker
    worker = True
    cookies = cookieParser()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")
    with thrd(max_workers=2) as subjob:
        subjob.submit(subJob_1, options, cookies, replUrl_1, "image_1.png")
        subjob.submit(subJob_2, options, cookies, replUrl_2, "image_2.png")

def subJob_1(options, cookies, replUrl, image):
    driver = webdriver.Chrome(options=options)
    driver.get("https://replit.com")
    firstLoop = True
    waitUntil = 15
    while True:
        driver.delete_all_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(replUrl)
        befTime = int(time.time())
        while True:
            sourceStop = re.search(">Stop<", driver.page_source)
            sourceRun = re.search(">Run<", driver.page_source)
            if sourceStop or sourceRun:
                break
            if int(time.time()) - befTime >= waitUntil:
                break
        driver.save_screenshot(image)
        if firstLoop:
            firstLoop = False
            waitUntil = 3

def subJob_2(options, cookies, replUrl, image):
    driver = webdriver.Chrome(options=options)
    driver.get("https://replit.com")
    firstLoop = True
    waitUntil = 15
    while True:
        driver.delete_all_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(replUrl)
        befTime = int(time.time())
        while True:
            sourceStop = re.search(">Stop<", driver.page_source)
            sourceRun = re.search(">Run<", driver.page_source)
            if sourceStop or sourceRun:
                break
            if int(time.time()) - befTime >= waitUntil:
                break
        driver.save_screenshot(image)
        if firstLoop:
            firstLoop = False
            waitUntil = 3

@app.route("/", methods=["GET"])
def index():
    if not worker:
        executor.submit(backgroundWorker)
    return f"{(int(time.time()) - waktuItu) // 60} menit telah dilalui, repl-mu masih tetap aktif 🥰"

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
