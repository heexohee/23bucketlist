# Flask 웹 애플리케이션을 구성하는 코드입니다. 
# 이 코드는 웹 서버를 실행하고, 클라이언트로부터 HTTP 요청을 받으면 해당 요청에 대한 응답을 반환합니다.

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.p77xisx.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


@app.route('/')  
    # '/' 경로는 홈 페이지를 나타내며, render_template 함수를 사용하여 'index.html' 템플릿을 렌더링하여 반환합니다.
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"]) 
    # '/bucket' 경로는 POST 요청을 받으면 버킷을 기록하는 함수인 bucket_post()를 실행합니다.
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num': count,
        'bucket': bucket_receive,
        'done': 0
    }

    db.bucket.insert_one(doc)

    return jsonify({'msg': '버킷 기록 했음!!!'}) 
# 버킷 기록을 처리하는 코드


@app.route("/bucket/done", methods=["POST"])
    # '/bucket/done' 경로는 POST 요청을 받으면 버킷을 완료 상태로 변경하는 함수인 bucket_done()를 실행합니다.
def bucket_done():
    num_receive = request.form['num_give']

    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})


    return jsonify({'msg': '버킷을 달성! ㅊㅊ'})
# 버킷 완료를 처리하는 코드


@app.route("/bucket", methods=["GET"])
    # '/bucket' 경로는 GET 요청을 받으면 현재 버킷 리스트를 반환하는 함수인 bucket_get()을 실행합니다.
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))

    return jsonify({'buckets': bucket_list}) 
# 버킷 리스트를 반환하는 코드

@app.route("/bucket/reset", methods=["POST"])
def bucket_reset():
    num_receive = request.form['num_give']

    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})

    return jsonify({'msg': '버킷 상태를 리셋했습니다.'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)

    # '/bucket' 경로는 GET 요청을 받으면 현재 버킷 리스트를 반환하는 함수인 bucket_get()을 실행합니다.
