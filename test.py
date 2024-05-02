import os
import time
import logging
import requests
import subprocess

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

config = {
    "baseApi": "http://127.0.0.1:6790",
    "appPackage": "com.android.chrome",
    "appActivity": "com.google.android.apps.chrome.Main"
}

def command(type, *args, **kwargs):
    requestData = kwargs.get('data', None)
    sessionId = kwargs.get('sessionId', None)
    elementId = kwargs.get('elementId', None)

    if type == "status":
        requestMethod = "get"
        requestUrl = "{0}/status".format(config['baseApi'])
    elif type == "createSession":
        requestMethod = "post"
        requestUrl = "{0}/session".format(config['baseApi'])
    elif type == "findElement":
        requestMethod = "post"
        requestUrl = "{0}/session/{1}/element".format(
            config['baseApi'], sessionId)
    elif type == "clickElement":
        requestMethod = "post"
        requestUrl = "{0}/session/{1}/element/{2}/click".format(
            config['baseApi'], sessionId, elementId)
    elif type == "inputElement":
        requestMethod = "post"
        requestUrl = "{0}/session/{1}/element/{2}/value".format(
            config['baseApi'], sessionId, elementId)
    elif type == "goBack":
        requestMethod = "post"
        requestUrl = "{0}/session/{1}/back".format(
            config['baseApi'], sessionId)

    if requestMethod == 'post':
        r = requests.post(requestUrl, json=requestData)
    else:
        r = requests.get(requestUrl, json=requestData)

    if r.ok:
        return r.json()
    else:
        raise Exception(r.json()["value"]["error"])


def permission(sessionId):
    try:
        time.sleep(1)
        logging.info("İzin bekleme click")

        # XPath ifadesiyle eşleşen öğeleri bul
        elements = command("findElement", sessionId=sessionId, data={
                "strategy": "xpath",
                "selector": "//android.widget.Button[@resource-id='android:id/button1']"
        })["value"]["ELEMENT"]

        command("clickElement", sessionId=sessionId, elementId=elements)
        logging.info("İzin verildi")
        return True
    except Exception as e:
        logging.error("İzin alınırken bir hata oluştu: {}".format(str(e)))
        return False

def run():
    subprocess.Popen(["su -c 'am force-stop io.appium.uiautomator2.server.test'"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    subprocess.Popen(["su -c 'nohup am instrument -w io.appium.uiautomator2.server.test/androidx.test.runner.AndroidJUnitRunner'"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

    time.sleep(10)
    logging.info("UIAutomator serverının çalışıp çalışmadığını kontrol ediliyor.")
    if not command('status'):
        raise Exception("UIAutomator sunucusu çalışmıyor.")

    logging.info("Yeni bir oturum oluşturuluyor.")
    sessionId = command("createSession", data={
        "capabilities": {}
    })["sessionId"]

    logging.info("Oturum ID'si: {}".format(sessionId))
    while True:
        os.system("su -c 'uiautomator dump view.xml'")

        if permission(sessionId):
            time.sleep(2)
            logging.info("İzin alındı.")
        else:
            logging.info("İzin alınamadı. Tekrar denenecek.")
            time.sleep(5)

try:
    while True:
        try:
            run()
        except Exception as e:
            logging.error(str(e))
            time.sleep(5)  # Hata oluştuğunda bekleme süresi ekleyebilirsiniz.
except KeyboardInterrupt:
    logging.info("Program sonlandırıldı.")
