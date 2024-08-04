from flask import Flask, request, jsonify
from flask_cors import cross_origin
import pvz
import json
app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
@cross_origin() 
def get_wa():
    return 'Hello World', 200  # 返回一个成功的消息
@app.route('/pvz', methods=['POST','GET'])
@cross_origin() 
def get_data():
    return pvz.get_pvz_url(),200
@app.route('/urls', methods=['POST','GET'])
@cross_origin() 
def urls():
    with open('config.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    for i in range(len(urls)):
        if '植物大战僵尸杂交版'in urls[i]["name"]:
            urls[i]["url"] = pvz.get_pvz_url()
            break
    return jsonify(urls),200
if __name__ == '__main__':
    app.run(host='localhost', port=3080)