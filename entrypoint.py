#!/bin/env python3
import os
import requests
import argparse
from tqdm import tqdm
from trevi_tools.aliyun_tools.oss_tools import Aliyun_OSS_Tools
from trevi_tools.gengu_signature.sign import gengu
from trevi_tools.gengu_signature.validation.ios_check import iOS_APP_Validation


class iOS_Sign(object):

    def __init__(self, productID, module_name, version_num):
        self.productID = productID
        self.module_name = module_name
        self.version_num = version_num

    def download_sign_ios_file(self, url, sign_dest_path):
        # stream=True的作用是仅让响应头被下载，连接保持打开状态
        resp = requests.get(url=url, stream=True)

        # 确定整个安装包的大小
        content_size = int(resp.headers['Content-Length']) / 1024

        with open(sign_dest_path, "wb") as f:
            print("安装包整个大小是：", content_size, 'k，开始下载...')

            # 調用iter_content， 一塊一塊的遍歷要下载的内容，搭配stream=True，此时才開始真正的下载
            # iterable：可迭代的進度條
            # total：總共迭代次數
            for data in tqdm(iterable=resp.iter_content(1024), total=content_size, unit='k'):
                f.write(data)


            print(sign_dest_path + "已经下载完毕！")

    def start(self):
        # 建立阿里云OSS物件實例(上傳下載功能另外封裝成物件以便調用)
        aliyunTools = Aliyun_OSS_Tools(productID=self.productID, module_name=self.module_name, version_num=self.version_num)

        try:
            # 從OSS上下載指定產品、模塊、版本
            aliyunTools.download_ipa_from_oss()

            # 建立亙古物件
            genguSignTools = gengu(productID=self.productID, module=self.module_name)

            # 登入
            os.system("echo ====================登入亙古API....====================\n")
            genguSignTools.login()

            # 上傳要簽名的檔案
            os.system("echo ====================上傳檔案到亙古簽名API....====================\n")
            genguSignTools.upload_unsign_file(filePath=aliyunTools.local_unsign_file_path)

            # 確認上傳狀態
            os.system("echo ====================查詢亙古檔案上傳是否成功的API....====================\n")

            if genguSignTools.check_upload_status():

                # 檢察檔案上傳成功
                os.system("echo ====================檔案上傳成功====================\n")

                # 確認簽名狀態
                os.system("echo ====================檢查簽名狀態....====================\n")
                genguSignTools.check_sign_status()

                # 請求簽名完成的下載鏈結
                os.system("echo ====================獲得下載鏈結====================\n")
                download_link = genguSignTools.get_download_link()

                # 開始進行下載
                os.system("echo ===================開始下載檔案....=========================\n")
                os.system("echo ===================檔案儲存路徑: %s =========================\n" % aliyunTools.local_sign_file_path)
                self.download_sign_ios_file(url=download_link, sign_dest_path=aliyunTools.local_sign_file_path)
                os.system("echo ===================檔案下載完成!!!!=========================\n")

                # 開始驗證包的正確性
                os.system("echo ===================開始進行驗證ipa包==========================\n")
                ios_validation_tool = iOS_APP_Validation(filePath=aliyunTools.local_sign_file_path, productID=self.productID,
                                                         module=self.module_name, version=self.version_num)

                if ios_validation_tool.analyze():
                    os.system("echo ===================驗證無誤!!!=================================\n")

                    os.system("echo ===================上傳至OSS bucket==========================\n")
                    # 上傳至OSS
                    if aliyunTools.upload_ipa_to_oss():

                        os.system("echo ===================上傳完成!!!==========================\n")

                    else:
                        os.system("echo ===================上傳失敗!!!==========================\n")

                else:
                    os.system("echo ===================驗證失敗!!!  不繼續上傳動作=================================\n")

            else:
                print("")


        except Exception as e:
            os.system("echo ==========================捕捉到例外!! ,以下為錯誤訊息==========================\n")
            os.system(e)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='new')

    parser.add_argument("--productID", "-P", required=True, help='產品ID', type=str)
    parser.add_argument("--module", "-M", required=True, help='模塊名稱(AMS/ARS/GAME)', type=str)
    parser.add_argument("--version", "-V", required=True, help='版本號', type=str)

    args = parser.parse_args()

    if args.productID and args.module and args.version:
        ios_sign_instance = iOS_Sign(productID=args.productID, module_name=args.module, version_num=args.version)
        ios_sign_instance.start()
