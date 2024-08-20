from flask import Flask, request, jsonify, Response
from flask_cors import cross_origin
import requests
import pvz
import json
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
@app.route('/proxy', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy():
    target_url = 'https://baidu.com'  # 修改为你要代理的URL
    response = requests.request(
        method=request.method,
        url=target_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for name, value in response.raw.headers.items()
               if name.lower() not in excluded_headers]
    
    return Response(response.content, response.status_code, headers)
if __name__ == '__main__':
    app.run(host='localhost', port=3000)