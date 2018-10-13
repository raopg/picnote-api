from flask import Flask, jsonify, request
import json
from flask_s3 import FlaskS3
import DatabaseUtilities

db = DatabaseUtilities.DatabaseUtilities()

app = Flask(__name__)
app.config['FLASKS3_BUCKET_NAME'] = 'picnoteimages'
s3app = FlaskS3()
s3app.init_app(app)
@app.route('/', methods=['GET'])
#Inner facing REST API with no docs. Simple landing page
def index():
    return jsonify({'response': '200', 'message' : 'landing page'})

@app.route('/api', methods=['GET'])

def api_landing():
    return jsonify({'response': '200','message':'Welcome to the picNote API!'})

@app.route('/api/<string:key>', methods = ['GET'])
'''Validates the API key appended to the URL. This function will be repeatedly called in each route to verify that the URL is built correctly by the end user'''
def authenticate_api_key(key):
    valid_keys = []
    with open('creds.json','r') as f:
        valid_keys = json.load(f)
    if valid_keys['username'] == key:
        return jsonify({'response':'200','message':'API Key Verified'})
    return jsonify({'response':'401','message':'Authentication failed: Illegal API Key'})

@app.route('/api/<string:key>/login', methods = ['POST'])
'''Logs the professor by taking the username and password. Returns the professor ID if the authentication is successful. 403 error if authentication fails'''
def login(key):
    response = authenticate_api_key(key)
    if(response['response'] != '200'):
        return response
    if request.method == "POST":
        username = request.form.getlist("username")
        password = request.form.getlist("password")
        prof_id = db.read_professor_id(username,password)
        if prof_id != None:
            return jsonify({'response':'200','prof_id':prof_id})
    return jsonify({'response':'403','message':'This function only supports the POST method'})


@app.route('/api/<string:key>/<string:prof_id>/prof_add_course', methods = ['POST'])
'''Allows a professor to add a course, and a list of sections. Professor ID is passed as a request paramater. Returns a course ID'''
def prof_add_course(key,prof_id):
    response = authenticate_api_key(key)
    if(response['response'] != '200'):
        return response
    if request.method == "POST":
        course_name = request.form.getlist("cname")
        section_list = request.form.getlist("slists")
        
        course_ID = db.write_course_entry(prof_id,course_name)
        for section_name in section_list:
            db.write_section_entry(course_ID,section_name)
        return jsonify({'response':'200','course_ID':course_ID})
    return jsonify({'response':'503','message':'Internal server error'})



@app.route('/api/<string:key>/<string:course_id>/post_note', methods=['POST'])
'''Posts a note with the course code supplied as a request parameter'''
def post_note(key,course_id):
    json_return = authenticate_api_key(key)
    if(json_return['response'] != '200'):
        return json_return
    if request.method == "POST":
        img_link = request.form.getlist("img_link")
        note_text = request.form.getlist("note_text")

        # Line [77] generates the s3 bucket link to store in the database

        s3_url = app.url_for(img_link) 
        db.write_note_entry(s3_url,note_text,course_id)
    
        

@app.route('/api/<string:key>/<string:hashed>/get_notes', methods=['GET'])
'''Gets notes depending on the request hash key. If the key belongs to none of the participating groups, returns a 404 error'''
def get_notes_by_id(key, hashed):
    json_return = authenticate_api_key(key)
    if(json_return['response'] != '200'):
        return json_return
    if db.prof_id_exists(hashed):
        return jsonify(db.read_notes_by_prof(hashed))
    elif db.course_id_exists(hashed):
        return jsonify(db.read_notes_by_course(hashed))
    elif db.section_id_exists(hashed):
        return jsonify(db.read_notes_by_section(hashed))
    else:
        return jsonify({'response':'404','message':'Hashed ID does not match a professor, student or section'})




if __name__ == '__main__':
    app.run(debug=True, port=8080)