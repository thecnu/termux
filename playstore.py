import os
import time
import logging
import datetime
import requests

#adb shell nohup am instrument -w io.appium.uiautomator2.server.test/androidx.test.runner.AndroidJUnitRunner

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

config = {
    "baseApi": "http://127.0.0.1:6790/wd/hub",
    "appPackage": "com.android.chrome",
    "appActivity": "com.google.android.apps.chrome.IntentDispatcher"
}

isAndroid = 'ANDROID_STORAGE' in os.environ or 'ANDROID_ROOT' in os.environ

try:
    # launch apps
    if isAndroid:
        os.system("am start -W -n {0}/{1} -S -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -f 0x10200000".format(
            config["appPackage"], config["appActivity"]))
    else:
        os.system("adb shell am start -W -n {0}/{1} -S -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -f 0x10200000".format(
            config["appPackage"], config["appActivity"]))

    def command(type, *args, **kwargs):
        requestData = kwargs.get('data', None)
        sessionId = kwargs.get('sessionId', None)
        elementId = kwargs.get('elementId', None)

        #if status == 200:


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

    logging.info("checking is uiautomator server running")
    if not command('status'):
        raise Exception("UIAutomator server not running.")

    logging.info("create new session")
    sessionId = command("createSession", data={
        "capabilities": {
        }
    })["sessionId"]

#


    def chrome1():
        try:

            time.sleep(1)
            logging.info("home click")
            elementId = command("findElement", sessionId=sessionId, data={
                "strategy": "id",
                "selector": "com.android.chrome:id/home_button"
            })["value"]["ELEMENT"]

            time.sleep(1)

            logging.info("home click ok")
            command("clickElement", sessionId=sessionId, elementId=elementId)


            time.sleep(1)
            logging.info("url click")
            elementId = command("findElement", sessionId=sessionId, data={
                "strategy": "id",
                "selector": "com.android.chrome:id/search_box_text"
            })["value"]["ELEMENT"]

            time.sleep(1)

            logging.info("url click ok")
            command("clickElement", sessionId=sessionId, elementId=elementId)

            time.sleep(1)

            logging.info("chrome input click")
            elementId = command("findElement", sessionId=sessionId, data={
                "strategy": "id",
                "selector": "com.android.chrome:id/url_bar"
            })["value"]["ELEMENT"]

            time.sleep(1)

            command("clickElement", sessionId=sessionId, elementId=elementId)

            time.sleep(1)


            command("inputElement", sessionId=sessionId, elementId=elementId, data={
            "text": "istanbul çilingir\\n"
            })
            # "\\n" enter komutu
            logging.info("chrome input click ok")

            '''
            # buraya konum 
            time.sleep(1)
            logging.info("bölge")
            elementId1 = command("findElement", sessionId=sessionId, data={
                    "strategy": "xpath",
                    "selector": "//android.widget.Button[1][@text='Bölge seç']"
          
            })["value"]["ELEMENT"]

            time.sleep(1)

            command("clickElement", sessionId=sessionId, elementId=elementId1)
            logging.info("bölge ok")



            time.sleep(3)
            logging.info("tam konum")
            elementId2 = command("findElement", sessionId=sessionId, data={
                    "strategy": "xpath",
                    "selector":"//android.widget.Button[1][@text='Tam konumu kullan']" 
          
            })["value"]["ELEMENT"]

            time.sleep(1)

            command("clickElement", sessionId=sessionId, elementId=elementId2)
            logging.info("tam konum ok")


            
            time.sleep(2)
            logging.info("chrome konum izin ver")
            elementId2 = command("findElement", sessionId=sessionId, data={
                    "strategy": "xpath",
                    "selector":'//android.widget.Button[contains(@text, "İzin ver")]' 
          
            })["value"]["ELEMENT"]

            time.sleep(1)

            command("clickElement", sessionId=sessionId, elementId=elementId2)
            logging.info("chrome konum izin ver ok")


            time.sleep(2)
            logging.info("telefon konum izin ver")
            elementId2 = command("findElement", sessionId=sessionId, data={
                    "strategy": "id",
                    "selector":"com.android.packageinstaller:id/permission_allow_button"
          
            })["value"]["ELEMENT"]

            time.sleep(1)

            command("clickElement", sessionId=sessionId, elementId=elementId2)
            logging.info("telefon konum izin ver ok")
            '''
            time.sleep(2)
            logging.info("ilk arama click")
            elementId2 = command("findElement", sessionId=sessionId, data={
                    "strategy": "xpath",
                    "selector": "//android.widget.Button[contains(@text, 'Telefon et')]"
          
            })["value"]["ELEMENT"]

            time.sleep(1)

            # Telefon et düğmesine tıklayın
            if elementId2:
                command("clickElement", sessionId=sessionId, elementId=elementId2)
            else:
                logging.error("Telefon et düğmesi bulunamadı")

           # command("clickElement", sessionId=sessionId, elementId=elementId2)
            logging.info("ilk arama click ok")







        except:
            print("hello")


        

    chrome1()

    logging.info("Done.")

except Exception as e:
        logging.error(str(e))
        if isAndroid:
            for x in range(3):
                command("goBack", sessionId=sessionId)
        else:
            os.system("adb shell am force-stop {0}".format(config["appPackage"]))
exit()


''' 
          logging.info("find hamburger icon element")
    elementId = command("findElement", sessionId=sessionId, data={
        "strategy": "id",
        "selector": "com.android.chrome:id/search_box_text"
    })["value"]["ELEMENT"]

    logging.info("click hamburger icon element (open drawer)")
    command("clickElement", sessionId=sessionId, elementId=elementId) 


        def chrome1():
        try:
            time.sleep(1)
            logging.info("chrome ilk")
            elementId = command("findElement", sessionId=sessionId, data={
            "strategy": "id",
            "selector": "com.android.chrome:id/empty_state_icon"
            })["value"]["ELEMENT"]

            time.sleep(1)

            logging.info("click hamburger icon element (open drawer)")
            command("clickElement", sessionId=sessionId, elementId=elementId)

            command("inputElement", sessionId=sessionId, elementId=elementId, data={
        "text": "try"
    })

        except:
            time.sleep(1)

            logging.info("chrome ilk except")
            elementId = command("findElement", sessionId=sessionId, data={
                "strategy": "id",
                "selector": "com.android.chrome:id/empty_state_icon"
            })["value"]["ELEMENT"]

            time.sleep(1)

        logging.info("click hamburger icon element (open drawer)")
        command("clickElement", sessionId=sessionId, elementId=elementId)

        command("inputElement", sessionId=sessionId, elementId=elementId, data={
        "text": "except"
    })

'''