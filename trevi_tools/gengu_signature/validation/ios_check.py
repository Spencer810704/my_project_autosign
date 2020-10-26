import os
import re
import zipfile
import plistlib


class iOS_APP_Validation(object):
    """
     一個ipa其實就是一個zip文件改了後綴名。如果你把ipa的後綴改回.zip，那麼你就能通過各種解壓軟件直接解壓了(或是7z可以直接壓縮)。

    目錄結構大概是這樣
    Payload
    |-- ...
    |-- ...
    |-- APP名稱.app
        |
        |-- ...
        |-- ...
        |-- Info.plist       <===== 紀錄app基本資訊
        |-- signTimeKey.txt  <===== 亙古簽名過後會產生這個簽名碼檔案
    """
    
    def __init__(self, filePath, productID, module, version ):
        
        # 建立Zipfile物件     
        self.ipa_file = zipfile.ZipFile(filePath)
        # 使用正規表示法取得Info.plist檔案 , 裡面記載了我們ipa的基本資訊 ,先取得ipa目錄結構列表之後傳給find_plist_file函式使用正規表示法找到Info.plist檔案實際路徑
        self.ipa_file_structure = self.ipa_file.namelist()

        self.productID = productID
        self.module = module
        self.version = version

        # self.filename = os.path.basename(filePath).split('.')[0]


    def analyze(self):
        if self.check_signature() and self.check_plist_info():            
            return True
        else:
            return False
        
    

    def check_signature(self):
        signKey_filePath_pattern = re.compile(r'Payload/[^/]*.app/signTimeKey.txt')
        signKey_path = self.find_specific_file(signKey_filePath_pattern)

        if signKey_path:
            signKey_file_content = self.ipa_file.read(signKey_path)
            os.system("echo 簽名碼:%s \n" % signKey_file_content.decode())
             
            return True

        else:
            os.system("echo 此IPA沒有簽名過 , 請重新簽名 \n")
            return False

    def check_plist_info(self):
        plist_filePath_pattern = re.compile(r'Payload/[^/]*.app/Info.plist')
        plist_path = self.find_specific_file(plist_filePath_pattern)
        # 使用zipfile套件將Info.plist檔案內容讀入 ,放置在plist_data變數內 
        plist_data = self.ipa_file.read(plist_path)
        
        # plistlib這個套件能夠處理zip類型的文件，並且可以在不解壓的情況下讀取裡面某個文件的內容。
        plist = plistlib.loads(plist_data)
        
        if self.module.lower().strip() == 'ams':
            os.system("echo ================Plist內容================= \n")
            os.system('echo Product Name: %s \n' % plist['ProductID'])
            os.system('echo Bundle Identifier: %s \n' % plist['CFBundleIdentifier'])
            os.system('echo Version: %s \n' % plist['CFBundleShortVersionString'])
            if plist['ProductID'].lower().strip() == self.productID.lower().strip() and plist['CFBundleShortVersionString'] == self.version:
                return True
            else:
                return False


        elif self.module.lower().strip() == 'game':
            os.system("echo ================Plist內容================= \n")
            os.system('echo Product Name: %s \n' % plist['TKProductID'])
            os.system('echo Bundle Identifier: %s \n' % plist['CFBundleIdentifier'])
            os.system('echo Version: %s \n' % plist['CFBundleShortVersionString'])

            if plist['TKProductID'].lower().strip() == self.productID.lower().strip() and plist['CFBundleShortVersionString'] == self.version:
                return True
            else:
                return False
        
        elif self.module.lower().strip() == 'ars':
            os.system("echo ================Plist內容================= \n")
            os.system('echo Product Name: %s \n' % plist['BusinessID'])
            os.system('echo Bundle Identifier: %s \n' % plist['CFBundleIdentifier'])
            os.system('echo Version: %s \n' % plist['CFBundleShortVersionString'])

            if plist['BusinessID'].lower().strip() == self.productID.lower().strip() and plist['CFBundleShortVersionString'] == self.version:
                return True
            else:
                return False
        
        elif self.module.lower().strip() == 'booking':
            os.system("echo ================Plist內容================= \n")
            os.system('echo Product Name: %s \n' % plist['BusinessID'])
            os.system('echo Bundle Identifier: %s \n' % plist['CFBundleIdentifier'])
            os.system('echo Version: %s \n' % plist['CFBundleShortVersionString'])

            if plist['BusinessID'].lower().strip() == self.productID.lower().strip() and plist['CFBundleShortVersionString'] == self.version:
                return True
            else:
                return False

    def find_specific_file(self, pattern):
        for path in self.ipa_file_structure:
            m = pattern.match(path)
            if m is not None:
                return m.group()
    
    
        
        
