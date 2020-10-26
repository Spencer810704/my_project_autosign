#!/bin/env python3
import os
import json
import time
import requests


class gengu(object):
    """
    (範例文件)
    
    ================ 產品的(遊戲、代理)對應id值  , 用於確認上傳ipa狀態是否成功 ========================
    # ID: ABCD => BBBB Game
    # ID: DDSS => NDSOAIN 代理

    # ID: ABCD => BBBB Game
    # ID: MDSK => MSDMS 代理

    # ID: DMASKODM => 其他 Game
    # ID: DMSKM => 其他 代理

    ================= 產品的(遊戲、代理)對應akey值 , 用於請求簽發狀態以及download link ================    
    # 龍門娛樂 game , akey = MDSOKMD 
    # 龍門代理 ams , akey = MSOKDMSAD

    # A88GD game , akey = MDOSKMDOAS
    # A88GD ams ,  akey = DMOSKMDA

    # 其他產品 game , akey = DMSOKMDAOD
    # 其他產品 ams  akey = MDOSAKMDOS


    """


    def __init__(self,productID,module):


        self.login_url = "http://www.tadsdsddaaadsadm0479.com/Bv1/login/logsin"
        self.upload_url = "http://saaaign.godasddceshi.com/Bv1/upload/index_uplog"
        self.check_upload_url = "http://sigaan.gocesdsadadhi.com/Bv1/upload/index_ipa"
        self.check_sign_status_url = "http://wwsdaw.tm0NJINJIda479.com/Bv1/Login/check_status"
        self.get_download_link_url = "http://wdadsww.tm0aNJONOsd479.com/Bv1/index/download"
        self.requests = requests.session()

        if productID.lower().strip() == 'sssss' or productID.lower().strip() == 'aasdsad':
            if module.lower().strip() == 'gasdame':
                self.akey = 'dassadads'
                self.id = '8dasd329'
            elif module.lower().strip() == 'amsadasds':
                self.akey = 'uasdasz2v'
                self.id = '84asdasda19'
        
        elif productID.lower().strip() == 'a8saddda8' or productID.lower().strip() == 'sdaa8dasas9':
            if module.lower().strip() == 'gsadaaame':
                self.akey = 'ddasdw1m'
                self.id = 'asd5990asd'
            elif module.lower().strip() == 'amsasd':
                self.akey = '2jadsdasv1'
                self.id = '5adads994'

        elif productID.lower().strip() == 'agdasdas':
            if module.lower().strip() == 'bookasdasding':
                self.akey = '7asdasdh99'
                self.id = '13asdad451'

            elif module.lower().strip() == 'arsasdas':
                self.akey = 'efdsgde2'
                self.id = '62erger228'

        else:
            if module.lower().strip() == 'asdadsafgame':
                self.akey = 'xfdagdsgp1a'
                self.id = '61gsdgsdg89'
            elif module.lower().strip() == 'amdsgsdgdsgs':
                self.akey = 'u7dfdsfe4'
                self.id = '6gsdgsdg204'
        

    def login(self):

        payload = {
            'mobile': 'fdasdffafvcwvrrwv',
            'pwd': 'fafdasdafewfwefe'
        }

        response = self.requests.post(url=self.login_url, data=payload)

        if response.status_code == 200:
            content = json.loads(response.text)
            if content['code'] == 200:
                self.token = content['data']['token']
                os.system("echo 登入成功, token為: %s \n" % self.token )


            else:
                os.system("echo 登入失敗! \n")
                os.system("echo 狀態碼: %s  \n" % content['code'])
                os.system("echo message : %s  \n" % content['msg'])

    def upload_unsign_file(self, filePath):
        
        # 讀取Binary file
        ipa_file = open(filePath, 'rb')

        data = {
            'app': ipa_file
        }

        response = self.requests.post(url=self.upload_url, files=data)

        # 判斷Request請求是否成功 , 並非亙古回傳的狀態碼
        if response.status_code == 200:
            # 請求成功後獲取json格式訊息
            content =json.loads(response.text)

            # 判斷亙古返回的Status code
            if content['code'] == 200:
                self.uri_path = content['data']['time']
                self.size = content['data']['size']
                self.upload_host = content['data']['upload_host']


                os.system("echo time = %s  \n" % self.uri_path )
                os.system("echo size = %s  \n" % self.size )
                os.system("echo upload_host = %s  \n" % self.upload_host )
        
            # 如果亙古不是返回200 , 打印出請求失敗原因
            else:
                os.system("echo status code = %s \n" % content['code'])
                os.system("echo message = %s  \n" % content['msg'])

    def check_upload_status(self):
        #==================== 檢查上傳是否成功 ===========================
      
        payload = {
            "time":self.uri_path,
            "size":self.size ,
            "upload_host":self.upload_host, 
            "id":self.id,
            "token":self.token
        }

        try:
            response = self.requests.post(url=self.check_upload_url, data=payload)

            if response.status_code == 200:

                content = json.loads(response.text)

                if content['code'] == '200':
                    self.akey = content['data']['akey']
                    return True
                else:
                    os.system("echo status code = %s \n" % content['code'])
                    os.system("echo message = %s  \n" % content['msg'])
                    return False

            else:
                return False

        except Exception as e:
            print(e)
            return False


    def check_sign_status(self):
        #===================== 獲取目前簽發狀態 ============================
         
        
        payload = {
            "akey": self.akey,
            # 此uid為固定值 , 但因為沒有亙古詳細API文檔 , 所以也不知道用途
            "uid": "11354"
        }

        status = 0 

        while(status != '2'):
            
            response = self.requests.post(url=self.check_sign_status_url, data=payload)
            
            if response.status_code == 200:
                content = json.loads(response.text)

                if content['code'] == 200:
                    status = content['data']['status']
                    os.system("echo 簽名中.....等待10秒後繼續查詢簽名狀態 \n")
                    time.sleep(10)
                else:
                    os.system("echo status code = %s \n" % content['code'])
                    os.system("echo message = %s  \n" % content['msg'])


        os.system("echo 簽名完成!!! \n")

    def get_download_link(self):
        #===================== 獲取簽發完成的下載鏈接 ============================
        os.system("echo 請求下載鏈結 \n")
        payload = {
            "akey": self.akey
        }

        response = self.requests.post(url=self.get_download_link_url, data=payload)
        
        if response.status_code == 200:
            content = json.loads(response.text)
            if content['code'] == 200:
                download_link =  content['url']
                os.system("echo download link: %s \n" % download_link)
                return download_link
            else:
                os.system("echo 獲取下載點失敗! \n")
                os.system("echo 狀態碼: %s  \n" % content['code'])
                os.system("echo message : %s \n" % content['msg'])



if __name__ == "__main__":
    # # 建立物件
    # gengu = gengu()
    
    # # 登入亙古
    # gengu.login()

    # # 檢查簽名狀態
    # gengu.check_sign_status()
    # gengu.get_download_link()

    pass
