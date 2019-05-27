from urllib import parse
import requests
import re
from lxml import etree
import os
from tqdm import tqdm

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
def parse_name(res):
    try:
        number = re.findall(r'<strong>(\d{1,2})</strong>',res)[1]
        print('当前共找到'+number+'条视频')
        data = etree.HTML(res)
        for i in range(0,int(number)):
            pic = data.xpath('//*[@class="video_box"]/a/img[1]/@src')[i]
            vname = data.xpath('//*[@class="video_box"]/a/img/@title')[i]
            vtime = data.xpath('//*[@class="video_box"]/div[1]/text()')
            url = data.xpath('//*[@class="video_box"]/a/@href')[i]
            vtime = [x for x in vtime if x!='\n'][i]
            # print('【'+vname+'|'+'时长:'+vtime+'|'+'图片预览地址:'+pic+'】')
            yield pic,vname,vtime,url,i
    except IndexError:
        print("暂未找到相关信息")

def load_html(name):
    url = 'https://www.thisav.com/search?cc=1&init=1&query={}&for=videos'
    name = parse.quote(name,encoding='utf-8')
    res = requests.get(url.format(name),headers = headers)
    res.encoding='utf-8'
    info = []
    for x in parse_name(res.text):
        pic, vname, vtime,url,i=x
        info.append(x)
        print(str(i+1)+'【'+vname+'|'+'时长:'+vtime+'|'+'图片预览地址:'+pic+'】')
    num = input('请输入要下载的序号：')
    pic, vname, vtime,url,i=info[int(num) - 1]
    download(load_url(url),vname)


def load_url(url):
    res = requests.get(url,headers=headers)
    md_url = str(re.findall(r'<source src=\"(.*?)\"',res.text)[0])
    return md_url.replace('.mpd','_dashinit.mp4')

def download(url, name):
    res = requests.get(url, stream=True, timeout=30)
    if os.path.exists('D:/1/%s.mp4' % (name)) == True:
        print('文件已存在')
        pass
    else:
        file_size = int(res.headers['content-length'])
        pdar = tqdm(ncols=70, total=file_size, desc=name, unit='it', unit_scale=True)
        with open(r'D:/1/%s.mp4' % (name), 'wb')as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
                pdar.update(1024)
        pdar.close()

if __name__ == '__main__':
    name = input("请输入搜索名字：")
    load_html(name)
