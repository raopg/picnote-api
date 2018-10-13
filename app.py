from flask import Flask, jsonify, request
import json

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
    if valid_keys['username'] == key:
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
        prof_id = db.login(username,password)
        if prof_id != None:
            return jsonify({'response':'200','prof_id':prof_id})
    return jsonify({'response':'403','message':'This function only supports the POST method'})


@app.route('/api/<string:key>/<string:hashed>/prof_add_course', methods = ['POST'])
def prof_add_course(key,hashed):
    response = authenticate_api_key(key)
    if(response['response'] != '200'):
        return response
    if request.method == "POST":
        course_name = request.form.getlist("cname")
        section_list = request.form.getlist("slists")
        
        course_ID = db.prof_add_course(hashed,cname)
        for section_name in section_list:
            db.prof_add_section(course_ID,section_name)
        return jsonify({'response':'200','course_ID':course_ID})
    return jsonify({'response':'503','message':'Internal server error'})



@app.route('/api/<string:key>/<string:hashed>/post_note', methods=['POST'])
def post_note(key,hashed):
    json_return = authenticate_api_key(key)
    if(json_return['response'] != '200'):
        return json_return
    if request.method == "POST":
        img_link = request.form.getlist("img_link")
        note_text = request.form.getlist("note_text")
        

@app.route('/api/<string:key>/<string:hashed>/get_notes', methods=['GET'])
def get_notes_by_id(key, hashed):
    json_return = authenticate_api_key(key)
    if(json_return['response'] != '200'):
        return json_return
    if db.prof_id_exists(hashed):
        return jsonify(db.get_prof_notes(hashed))
    elif db.course_id_exists(hashed):
        return jsonify(db.get_course_notes(hashed))
    elif db.section_id_exists(hashed):
        return jsonify(db.get_section_notes(hashed))
    else:
        return jsonify({'response':'404','message':'Hashed ID does not match a professor, student or section'})




if __name__ == '__main__':
    app.run(debug=True, port=8080)