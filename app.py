from flask import Flask, request, jsonify
from flask_cors import cross_origin
import requests
app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
@cross_origin() 
def get_wa():
    return 'Hello World', 200  # 返回一个成功的消息
@app.route('/data', methods=['POST','GET'])
@cross_origin() 
def get_data():
    res=requests.get('https://www.295yhw.com/video/8897.html')
    return res.content
if __name__ == '__main__':
    app.run(host='localhost', port=3080)