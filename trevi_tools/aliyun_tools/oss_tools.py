#!/bin/env python3
# -*- coding: utf-8 -*-
import os 
import oss2
import configparser



class Aliyun_OSS_Tools(object):

    def __init__(self, productID, module_name, version_num):
       
        self.config = configparser.ConfigParser()
        self.config.read('/opt/scripts/ios_automatic_sign/trevi_tools/aliyun_tools/config.ini')
        self.authentication()
        
        self.productID = productID
        self.module_name = module_name
        self.version_num = version_num
        # 取出子版本, 例:3.0.1160  , 取1160的值
        self.sub_version_num = version_num.split(".")[2]

        # Endpoint
        self.bucket_name = "ios-service-package"
        self.bucket = oss2.Bucket(self.auth, endpoint='http://oss-cn-hongkong.aliyuncs.com',bucket_name=self.bucket_name )
        
        if self.module_name.lower().strip() == 'ams':
            self.download_oss_object_name  = 'ios-{module}-rel/{sub_version}/AMS_{productID}_{version}.ipa'.format(module=module_name,sub_version=self.sub_version_num , productID=productID, version=version_num)
            self.upload_oss_object_name = 'sign-{module}/{sub_version}/AMS_{productID}_{version}.ipa'.format(module=module_name,sub_version=self.sub_version_num , productID=productID, version=version_num)
            
            # 取得game unsign的目錄路徑
            self.unsign_folder = self.config.get('unsign', 'ams')
            self.unsign_folder = os.path.join(self.unsign_folder,self.sub_version_num)
            self.create_folder_if_not_exist(self.unsign_folder)
            
            # 取得game sign的目錄路徑
            self.sign_folder = self.config.get('sign', 'ams')
            self.sign_folder = os.path.join(self.sign_folder,self.sub_version_num)
            self.create_folder_if_not_exist(self.sign_folder)

            self.local_filename = 'AMS_{productID}_{version}.ipa'.format(productID=self.productID, version=self.version_num)
            self.local_unsign_file_path = os.path.abspath((os.path.join(self.unsign_folder, self.local_filename )))
            self.local_sign_file_path = os.path.abspath((os.path.join(self.sign_folder, self.local_filename )))

        elif self.module_name.lower().strip() == 'game':
            
            self.download_oss_object_name  = 'ios-{module}-rel/{sub_version}/PhoneClient_{productID}_{version}.ipa'.format(module=module_name,sub_version=self.sub_version_num , productID=productID, version=version_num)
            self.upload_oss_object_name  = 'sign-{module}/{sub_version}/PhoneClient_{productID}_{version}.ipa'.format(module=module_name,sub_version=self.sub_version_num , productID=productID, version=version_num)
            # 取得game unsign的目錄路徑
            self.unsign_folder = self.config.get('unsign', 'game')
            self.unsign_folder = os.path.join(self.unsign_folder,self.sub_version_num)
            self.create_folder_if_not_exist(self.unsign_folder)
            
            # 取得game sign的目錄路徑
            self.sign_folder = self.config.get('sign', 'game')
            self.sign_folder = os.path.join(self.sign_folder,self.sub_version_num)
            self.create_folder_if_not_exist(self.sign_folder)

            
            # 儲存在本地的檔案名稱(不含路徑 , 只有檔案名稱及副檔名)
            self.local_filename = 'PhoneClient_{productID}_{version}.ipa'.format(productID=self.productID, version=self.version_num)
            self.local_unsign_file_path = os.path.abspath((os.path.join(self.unsign_folder, self.local_filename )))
            self.local_sign_file_path = os.path.abspath((os.path.join(self.sign_folder, self.local_filename )))

        elif self.module_name.lower().strip() == 'ars':
            
            self.download_oss_object_name  = 'ios-{module}-rel/{sub_version}/ARS-{productID}-{version}.ipa'.format(module=module_name,sub_version=self.sub_version_num , productID=productID, version=version_num)
            self.upload_oss_object_name  = 'sign-{module}/{sub_version}/ARS-{productID}-{version}.ipa'.format(module=module_name,sub_version=self.sub_version_num , productID=productID, version=version_num)
            
            # 取得game unsign的目錄路徑
            self.unsign_folder = self.config.get('unsign', 'ars')
            self.unsign_folder = os.path.join(self.unsign_folder,self.sub_version_num)
            self.create_folder_if_not_exist(self.unsign_folder)
            
            # 取得game sign的目錄路徑
            self.sign_folder = self.config.get('sign', 'ars')
            self.sign_folder = os.path.join(self.sign_folder,self.sub_version_num)
            self.create_folder_if_not_exist(self.sign_folder)

            
            # 儲存在本地的檔案名稱(不含路徑 , 只有檔案名稱及副檔名)
            self.local_filename = 'ARS-{productID}-{version}.ipa'.format(productID=self.productID, version=self.version_num)
            self.local_unsign_file_path = os.path.abspath((os.path.join(self.unsign_folder, self.local_filename )))
            self.local_sign_file_path = os.path.abspath((os.path.join(self.sign_folder, self.local_filename )))

        elif self.module_name.lower().strip() == 'booking':
            
            self.download_oss_object_name  = 'ios-{module}-rel/{sub_version}/BOOKING-{productID}-{version}.ipa'.format(module=module_name,sub_version=self.sub_version_num , productID=productID, version=version_num)
            self.upload_oss_object_name  = 'sign-{module}/{sub_version}/BOOKING-{productID}-{version}.ipa'.format(module=module_name,sub_version=self.sub_version_num , productID=productID, version=version_num)
            
            # 取得game unsign的目錄路徑
            self.unsign_folder = self.config.get('unsign', 'booking')
            self.unsign_folder = os.path.join(self.unsign_folder,self.sub_version_num)
            self.create_folder_if_not_exist(self.unsign_folder)
            
            # 取得game sign的目錄路徑
            self.sign_folder = self.config.get('sign', 'booking')
            self.sign_folder = os.path.join(self.sign_folder,self.sub_version_num)
            self.create_folder_if_not_exist(self.sign_folder)

            
            # 儲存在本地的檔案名稱(不含路徑 , 只有檔案名稱及副檔名)
            self.local_filename = 'BOOKING-{productID}-{version}.ipa'.format(productID=self.productID, version=self.version_num)
            self.local_unsign_file_path = os.path.abspath((os.path.join(self.unsign_folder, self.local_filename )))
            self.local_sign_file_path = os.path.abspath((os.path.join(self.sign_folder, self.local_filename )))


        else:
            os.system("echo ==================物件初始化時 , 請確認輸入模塊名稱正確(game/ams/)==================\n")

            self.download_oss_object_name = None
            self.unsign_folder = None
            self.sign_folder = None
            self.local_filename = None
    

    def authentication(self):
        # 建立auth物件
        access_key_id = self.config.get('auth', 'access_key_id')
        access_key_secret = self.config.get('auth', 'access_key_secret')

        self.auth = oss2.Auth(access_key_id, access_key_secret)

    def create_folder_if_not_exist(self,path):
        if not os.path.exists(path):
                os.makedirs(path)


    def download_ipa_from_oss(self):
        
        if self.local_unsign_file_path:
            os.system("echo ================== 從 %s Aliun OSS Bucket下載 ........==================\n" % self.bucket_name)
            os.system("echo ==================unsign ios app 本地路徑 : %s ==================\n"         % self.local_unsign_file_path)
        
            self.bucket.get_object_to_file(self.download_oss_object_name, self.local_unsign_file_path)
            os.system("echo ===================檔案下載完成!!!=============================\n")



    def upload_ipa_to_oss(self):
       
        try:
            if self.local_sign_file_path:
                os.system("echo ==================sign ios app 本地路徑 : %s ==================\n" % self.local_sign_file_path)
                os.system("echo ==================上傳ipa檔案到 %s Aliyun OSS Bucket........==================\n" % self.bucket_name)
                
            
                self.bucket.put_object_from_file(self.upload_oss_object_name, self.local_sign_file_path)
                os.system("echo ===================檔案上傳完成!!!=============================\n")

                return True

        except Exception as e:
            os.system("echo ====================上傳失敗.....捕捉到例外!!====================\n")
            os.system("Error Message: %s\n" % e)
            return False




if __name__ == "__main__":

    # 建立物件
    aliyun_tools = Aliyun_OSS_Tools(productID='A88GD',module_name='game', version_num='3.0.1160')

    # 下載請求
    aliyun_tools.download_ipa_from_oss()