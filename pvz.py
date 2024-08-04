import requests
import re
def get_pvz_url():
    res=requests.get('https://pvzgame.net/')
    txt=res.text
    pvz_url=re.findall('href="(.*?)">',txt)[4]
    return pvz_url