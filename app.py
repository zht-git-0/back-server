from flask import Flask, request, jsonify
from flask_cors import cross_origin
import asyncio
from playwright.async_api import async_playwright
import os
os.system('playwright install')
app = Flask(__name__)
async def fetch_url(url, context,i):
    page = await context.new_page()  
    page.set_default_timeout(600000)
    async def on_response(response):
        if target_url in response.url:
            video_urls[i]=response.url
            await page.close()
    page.on('response', on_response)
    try:await page.goto(url)
    except:None
async def main(base_url):  
    global video_urls,target_url
    p_id=base_url.split('/')[-1].split('.')[0]
    e=13
    target_url = "https://v16m-default.akamaized.net/"
    video_urls = [0 for i in range(e-1)]
    async with async_playwright() as p:    
        browser = await p.chromium.launch(headless=True)  
        context = await browser.new_context()  # 共享上下文
        urls = [f"https://www.295yhw.com/play/{p_id}-1-{i}.html" for i in range(1, e)]
        tasks = [fetch_url(urls[i],context,i) for i in range(len(urls))]  
        await asyncio.gather(*tasks)
        await context.close()  # 在所有任务完成后关闭上下文
        await browser.close()
        return video_urls
@app.route('/', methods=['POST','GET'])
@cross_origin() 
def get_wa():
    return 'Hello World', 200  # 返回一个成功的消息
@app.route('/data', methods=['POST','GET'])
@cross_origin() 
def get_data():
    base_url='https://www.295yhw.com/video/7592.html'
    return asyncio.run(main(base_url)), 200  # 返回一个成功的消息
if __name__ == '__main__':
    app.run(host='localhost', port=3080)