from flask import Flask, request, jsonify, Response, render_template_string
from flask_cors import cross_origin
import requests
import pvz
import json
import re
from bs4 import BeautifulSoup
app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
@cross_origin() 
def index():
    with open('config.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    return jsonify(urls),200
@app.route('/urls', methods=['POST','GET'])
@cross_origin() 
def push_urls():
    with open('config.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    for i in range(len(urls)):
        if '植物大战僵尸杂交版'in urls[i]["name"]:
            urls[i]["url"] = pvz.get_pvz_url()
            break
    return jsonify(urls),200
@app.route('/update', methods=['POST','GET'])
@cross_origin() 
def append():
    name = request.args.get('name')
    url = request.args.get('url')
    detail = request.args.get('detail')
    with open('config.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    for i in range(len(urls)):
        if urls[i]["name"] == name:
            urls[i]["detail"] = detail
            urls[i]["url"] = url
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(urls, f, ensure_ascii=False, indent=4)
            return jsonify(urls), 200
    urls.append({"name":name,"url":url,"detail":detail})
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(urls, f, ensure_ascii=False, indent=4)
    return jsonify(urls), 200
@app.route('/delete', methods=['POST','GET'])
@cross_origin() 
def delete():
    name = request.args.get('name')
    with open('config.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    for i in range(len(urls)):
        if urls[i]["name"] == name:
            urls.pop(i)
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(urls, f, ensure_ascii=False, indent=4)
            return jsonify(urls), 200
    return jsonify(urls), 200
@app.route('/search', methods=['POST','GET'])
@cross_origin() 
def search():
    name = request.args.get('name')
    res=[]
    with open('config.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    for i in range(len(urls)):
        if name in urls[i]["name"]:
            res.append(urls[i])
    if res != []:
        return jsonify(res), 200
    else:
        return jsonify({"message":"not found"}), 404
#http://localhost:3000/proxy?url=https://www.baidu.com
@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return "URL is required", 400

    try:
        headers = {
            'User-Agent': request.headers.get('User-Agent', 'Mozilla/5.0'),
            'referer': request.referrer
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 处理HTML内容
        if 'text/html' not in response.headers.get('Content-Type', ''):
            return "The URL does not return an HTML content", 400

        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        # 替换 href 和 src 属性中的 URL
        for tag in soup.find_all(['a', 'img', 'script']):
            if tag.name == 'a' and tag.has_attr('href'):
                href = tag['href']
                if href.startswith('http'):
                    tag['href'] = f'https://zht-back-server.us.kg/proxy?url={href}'
            elif tag.name in ['img', 'script'] and tag.has_attr('src'):
                src = tag['src']
                if src.startswith('http'):
                    tag['src'] = f'https://zht-back-server.us.kg/proxy?url={src}'

        modified_html_content = str(soup)
        return Response(modified_html_content, content_type='text/html; charset=utf-8')

    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve the page: {e}", 500
if __name__ == '__main__':
    app.run(host='localhost', port=3000)