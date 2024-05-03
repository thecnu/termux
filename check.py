import os
import time
import logging
import datetime
import requests
import subprocess
import asyncio

# adb shell nohup am instrument -w io.appium.uiautomator2.server.test/androidx.test.runner.AndroidJUnitRunner

# su -c pm grant com.termux android.permission.WRITE_SECURE_SETTINGS

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

config = {
    "baseApi": "http://127.0.0.1:6790",
    "appPackage": "com.android.chrome",
    "appActivity": "com.google.android.apps.chrome.Main"
}

isAndroid = 'ANDROID_STORAGE' in os.environ or 'ANDROID_ROOT' in os.environ

async def command(type, *args, **kwargs):
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

async def permission(sessionId):
    try:
        await asyncio.sleep(1)
        logging.info("izin bekleme click")

        # XPath ifadesiyle eşleşen öğeleri bul
        elements = (await command("findElement", sessionId=sessionId, data={
            "strategy": "xpath",
            "selector": "//android.widget.Button[@resource-id='android:id/button1']"
        }))["value"]["ELEMENT"]

        await command("clickElement", sessionId=sessionId, elementId=elements)
        logging.info("izin verildi")
        return True
    except Exception as e:
        logging.error(f"Permission error: {e}")
        return False

async def run():
    await asyncio.create_subprocess_shell("su -c 'am force-stop io.appium.uiautomator2.server.test'")
    await asyncio.create_subprocess_shell("su -c 'nohup am instrument -w io.appium.uiautomator2.server.test/androidx.test.runner.AndroidJUnitRunner'")

    await asyncio.sleep(10)
    logging.info("checking is uiautomator server running")
    if not await command('status'):
        raise Exception("UIAutomator server not running.")

    logging.info("create new session")
    sessionId = (await command("createSession", data={
        "capabilities": {}
    }))["sessionId"]

    logging.info(str(sessionId))
    while True:
        os.system("su -c 'uiautomator dump view.xml'")
        if await permission(sessionId):  # İzin verildiyse devam et
            logging.info("İzin verildi.")
            await asyncio.sleep(2)
        else:
            logging.info("İzin verilmedi.")
            await asyncio.sleep(5)

try:
    asyncio.run(run())

except Exception as e:
    logging.error(str(e))
    asyncio.run(run())
