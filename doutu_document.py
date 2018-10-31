import requests
from lxml import etree
from time import sleep
from concurrent import futures

url = 'http://www.doutula.com/article/list/?page=2'
headers = {
    'Referer':'http://www.doutula.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
}
def parse_page(url):
    resp = requests.get(url,headers=headers)
    html = etree.HTML(resp.text)
    imgs = html.xpath('.//div[@class="col-sm-9"]//img/@data-original')
    for img in imgs:
        try:
            download_img(img)
        except:
            pass
    if imgs:
        return True
    else:
        return False

def download_img(src):
    filename = src.split('/')[-1]
    img = requests.get(src, headers=headers)
    # img是图片响应，不能字符串解析;
    # img.content是图片的字节内容
    with open('img/' + filename, 'wb') as file:
        file.write(img.content)
    # print(src, filename)

base_url = 'http://www.doutula.com/article/list/?page={}'
i = 1
error_time = 0
next_link = True
while next_link:
    sleep(0.5)
    try:
        next_link = parse_page(base_url.format(i))
    except:
        next_link = True
    if next_link :
        i += 1
        error_time = 0
    else:
        if error_time>=3:
            print(error_time,'break')
            break
        i+=1
        error_time+=1
        next_link = True
    print(i,error_time)
print('~OVER~')