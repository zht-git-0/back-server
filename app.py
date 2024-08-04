from flask import Flask, request, jsonify
from flask_cors import cross_origin
import os
app = Flask(__name__)
@app.route('/data', methods=['POST','GET'])
@cross_origin()
def get_wa():
    return 'Hello World', 200  # 返回一个成功的消息
if __name__ == '__main__':
    app.run(host='localhost', port=3080)