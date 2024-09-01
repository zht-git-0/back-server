from flask import Flask, request, jsonify, Response, render_template_string
from flask_cors import cross_origin
from flask_caching import Cache
import requests
import pvz
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
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
def request_url(request,url):
    def modify_js(js_content):
        # 在这里你可以修改 JavaScript 内容
        # 例如替换所有的 URL
        js_content = js_content.decode('utf-8')  # 转换为字符串
        modified_js_content = re.sub(
            r'(http[s]?://[^\s"\']+)',  # 匹配 http:// 或 https:// 后面跟随的 URL
            lambda match: f'{request.base_url}?url={match.group(0)}',
            js_content
        )
        return modified_js_content.encode('utf-8')  # 转换回字节流
    if not url:
        return "URL is required", 400

    try:
        # 获取请求头中的 User-Agent 和 referer
        headers = {
            'User-Agent': request.headers.get('User-Agent', 'Mozilla/5.0'),
            'Referer': request.referrer,
            'Accept-Language': request.headers.get('Accept-Language'),
        }
        # 发起请求并获取响应
        response = requests.request(method=request.method, url=url, headers=headers)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '')
        content = response.content

        # 处理 HTML 内容
        if 'text/html' in content_type:
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')

            # 替换 href 和 src 属性中的 URL
            for tag in soup.find_all(['a', 'img', 'script', 'link']):
                if tag.name == 'a' and tag.has_attr('href'):
                    href = tag['href']
                    # 使用 urljoin 处理相对路径
                    new_url = urljoin(url, href)
                    # 使用 base_url 构造代理路径
                    tag['href'] = f'{request.base_url}?url={new_url}'
                elif tag.name in ['img', 'script'] and tag.has_attr('src'):
                    src = tag['src']
                    # 使用 urljoin 处理相对路径
                    new_url = urljoin(url, src)
                    # 使用 base_url 构造代理路径
                    tag['src'] = f'{request.base_url}?url={new_url}'
                elif tag.name == 'link' and tag.has_attr('href'):
                    href = tag['href']
                    # 使用 urljoin 处理相对路径
                    new_url = urljoin(url, href)
                    # 使用 base_url 构造代理路径
                    tag['href'] = f'{request.base_url}?url={new_url}'

            modified_html_content = str(soup)
            return Response(modified_html_content, content_type='text/html; charset=utf-8')
        # 处理 JavaScript 内容
        elif 'application/javascript' in content_type or 'text/javascript' in content_type:
            modified_js_content = modify_js(content)
            return Response(modified_js_content, content_type='application/javascript')

        # 处理其他内容
        else:
            mime_type = content_type
            return Response(content, content_type=mime_type)

    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve the page: {e}", 500
@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    return request_url(request, url)
if __name__ == '__main__':
    app.run(host='localhost', port=3000)