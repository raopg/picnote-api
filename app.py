from flask import Flask, jsonify, request
import authenticate
from professoraccount import Professor
from note import Note
firebase_app = authenticate.authenticate_firebase()

db = firebase_app.database()

app = Flask(__name__)
@app.route('/', methods=['GET'])
#Inner facing REST API with no docs. Simple landing page
def index():
    return jsonify({'response': '200', 'message' : 'landing page'})

@app.route('/api', methods=['GET'])

def api_landing():
    return jsonify({'response': '200','message':'Welcome to the picNote API!'})

@app.route('/api/<string:key>', methods = ['GET'])
def authenticate_api_key(key):
    valid_keys = []
    with open('creds.json','r') as f:
        valid_keys = json.load(f)
    if valid_keys['test'] == key:
        return jsonify({'response':'200','message':'API Key Verified'})
    return jsonify({'response':'401','message':'Authentication failed: Illegal API Key'})

@app.route('/api/<string:key>/login', methods = ['POST'])
def login(key):
    response = authenticate_api_key(key)
    if(response['response'] != '200'):
        return response
    if request.method == "POST":
        username = request.form.getlist("username")
        password = request.form.getlist("password")
        
    return jsonify({'response':'403','message':'This function only supports the POST method'})
@app.route('/api/<string:key>/<string:hashed>/add_course', methods = ['POST'])
def add_course(key,hashed):
    response = authenticate_api_key(key)
    if(response['response'] != '200'):
        return response
    if request.method == "POST":
        course_name = request.form.getlist("cname")
        section_list = request.form.getlist("slist")
        

@app.route('/api/<string:key>/<string:hashed>/post_note', methods=['POST'])
def post_note(key,hashed):
    json_return = authenticate_api_key(key)
    if(json_return['response'] != '200'):
        return json_return
    if request.method == "POST":
        img_link = request.form.getlist("img_link")
        note_text = request.form.getlist("note_text")
        

@app.route('/api/<string:key>/<string:hashed>/get_notes', methods=['GET'])
def get_notes(key, hashed):
    json_return = authenticate_api_key(key)
    if(json_return['response'] != '200'):
        return json_return
    return 



if __name__ == '__main__':
    app.run(debug=True, port=8080)