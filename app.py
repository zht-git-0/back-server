from flask import Flask, request, jsonify, Response, render_template_string
from flask_cors import cross_origin
import requests
import pvz
import json
import re
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
@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return "URL is required", 400

    try:
        response = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve the page: {e}", 500
    pattern = re.compile(r'(<a\s+[^>]*href=["\'])([^"\']+)(["\'])')
    # 使用正则表达式替换href值
    modified_html_content = pattern.sub(r'\1https://zht-back-server.us.kg/proxy?url=\2\3', str(response.content, 'utf-8'))
    return render_template_string(modified_html_content)
if __name__ == '__main__':
    app.run(host='localhost', port=3000)