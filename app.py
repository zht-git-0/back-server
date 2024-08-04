from flask import Flask, request, jsonify
from flask_cors import cross_origin
from get_url.main import main_thread
app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
@cross_origin() 
def get_wa():
    return 'Hello World', 200  # 返回一个成功的消息
@app.route('/data', methods=['POST','GET'])
@cross_origin() 
def get_data():
    base_url='https://www.295yhw.com/video/7592.html'
    return "1", 200  # 返回一个成功的消息
if __name__ == '__main__':
    app.run(host='localhost', port=3080)