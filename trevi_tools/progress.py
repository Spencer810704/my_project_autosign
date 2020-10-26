#!/usr/bin/env python


# File name: test_download.py
# Author: Spencer Chen
# Date created: 2019-10-22
# Date last modified: 
# Python Version: 3,6


import requests
from tqdm import tqdm


def downloadFile(url, name):

    # stream=True的作用是仅让响应头被下载，连接保持打开状态
    resp = requests.get(url=url, stream=True)

    # 确定整个安装包的大小
    content_size = int(resp.headers['Content-Length'])/1024

    with open(name, "wb") as f:
        print("安装包整个大小是：", content_size, 'k，开始下载...')

        # 调用iter_content，一块一块的遍历要下载的内容，搭配stream=True，此时才开始真正的下载
        # iterable：可迭代的进度条
        # total：总的迭代次数
        # desc：进度条的前缀
        for data in tqdm(iterable=resp.iter_content(1024), total=content_size, unit='k', desc=name):
            f.write(data)
        print(name + "已经下载完毕！")


if __name__ == '__main__':
    url = "http://sign.goceshi.com/App/info/download_app_v2/akey/dw1m.html?token=08a3d3304cae11f585004da7e1d1de20"
    name = url.split('/')[-1]
    # 截取整个url最后一段即文件名
    downloadFile(url, name)

