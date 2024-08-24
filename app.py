from flask import Flask, request, jsonify, Response, render_template_string
from flask_cors import cross_origin
import requests
import pvz
import json
import re
from bs4 import BeautifulSoup
import mimetypes
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
        # 获取请求头中的 User-Agent 和 referer
        headers = {
            'User-Agent': request.headers.get('User-Agent', 'Mozilla/5.0'),
            'Referer': request.referrer,
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        # 发起请求并获取响应
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 获取响应内容和类型
        content_type = response.headers.get('Content-Type', '')
        content = response.content
        mime_type, _ = mimetypes.guess_type(url)
        # 处理 HTML 内容
        if 'text/html' in content_type:
            soup = BeautifulSoup(content, 'html.parser')

            # 替换 href 和 src 属性中的 URL
            for tag in soup.find_all(['a', 'img', 'script']):
                if tag.name == 'a' and tag.has_attr('href'):
                    href = tag['href']
                    if href.startswith('http'):
                        tag['href'] = f'{request.path}?url={href}'
                elif tag.name in ['img', 'script'] and tag.has_attr('src'):
                    src = tag['src']
                    if src.startswith('http'):
                        tag['src'] = f'{request.path}?url={src}'
            modified_html_content = str(soup)
            return Response(modified_html_content, content_type='text/html; charset=utf-8')

        # 处理非 HTML 内容
        else:
            # 尝试猜测 MIME 类型
            mime_type, _ = mimetypes.guess_type(url)
            if mime_type is None:
                mime_type = content_type

            # 如果 MIME 类型未知或为空，则使用响应头中的内容类型
            if not mime_type:
                mime_type = content_type

            # 返回内容
            return Response(content, content_type=mime_type)

    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve the page: {e}", 500
if __name__ == '__main__':
    app.run(host='localhost', port=3000)