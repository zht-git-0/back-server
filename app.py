from flask import Flask, request, jsonify
from flask_cors import cross_origin
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
def urls():
    with open('config.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    for i in range(len(urls)):
        if '植物大战僵尸杂交版'in urls[i]["name"]:
            urls[i]["url"] = pvz.get_pvz_url()
            break
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(urls, f, ensure_ascii=False, indent=4)
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
if __name__ == '__main__':
    app.run(host='localhost', port=3080)