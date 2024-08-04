import requests
from lxml import etree
import re
def get_max_e(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    res=requests.get(url,headers=headers)
    html=etree.HTML(res.content)
    max_e=0
    title=re.findall('《.*?》',html.xpath('/html/head/title/text()')[0])[0]
    i=0
    while True:
        i+=1
        try:
            e=int(html.xpath(f'//*[@id="hl-plays-list"]/li[{i}]/a/@href')[0].split('/')[-1].split('.')[0].split('-')[-1])
        except:
            max_e=e
            break
    return max_e+1,title
def print_list(lis):
    print('[')
    for i in range(len(lis)):
        print(f"'{lis[i]}'")
    print(']')
