from flask import Flask, jsonify, request,render_template, redirect
import json
#from DatabaseUtilities import DatabaseUtilities
from flask_s3 import FlaskS3
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename

#db = DatabaseUtilities()

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = './static/img'
configure_uploads(app,photos)
s3_app = FlaskS3()
s3_app.init_app(app)
app.config['FLASKS3_BUCKET_NAME'] = 'picnoteimages'

#Loads credentials for the API key for the single user (assumption of one user for testing)
# with open('creds.json','r') as f:
#     valid_keys = json.load(f)

# #Authenticates users based on the API key usage
# def authenticate_api_key(key):
#     if valid_keys['username'] == key:
#         return {'response':'200','message':'API Key verified'}
#     return {'response':'401','message':'Authentication failed:Illegal API key'}

# #Inner facing RESTful API for picNote database access. Simple landing page
# @app.route('/', methods=['GET'])
# def index():
#     return jsonify({'response': '200', 'message' : 'landing page'})

# @app.route('/api', methods=['GET'])
# def api_landing():
#     return jsonify({'response': '200','message':'Welcome to the picNote API!'})

# '''Validates the API key appended to the URL. This function will be repeatedly called in each route to verify that the URL is built correctly by the end user'''
# @app.route('/api/<string:key>', methods = ['GET'])
# def authenticate(key):
#     #TODO: Move authentication to separate method and have it return a dict
#     #TODO: Make the actual handler function, be responsible for returning jsonify
#     #TODO: POTENTIAL ISSUES WITH LOCKING. MAKE SURE TO MOVE THIS FILE OPENING TO THE TOP OF THE APP WHEN YOU LOAD UP
    
#     #TODO: FIX BECAUSE IT GIVES ISSUES WITH
#     return jsonify(authenticate_api_key(key))

    

# '''Logs the professor by taking the username and password. Returns the professor ID if the authentication is successful. 403 error if authentication fails'''
@app.route('/api/<string:key>/login', methods = ['POST'])
def login(key):
    #response = authenticate_api_key(key)
    #if(response['response'] != '200'):
        # return jsonify(response)
    #if request.method == "POST":
        # username = request.form["username"]
        # password = request.form["password"]
        # prof_id = 123#db.read_professor_id(username,password)
        # if prof_id != None:
    return redirect("/{}/class".format(1))#{'response':'200','prof_id':prof_id})
    return jsonify({'response':'403','message':'This function only supports the POST method'})

# '''Allows a professor to add a course, and a list of sections. Professor ID is passed as a request paramater. Returns a course ID'''
# @app.route('/api/<string:key>/<string:prof_id>/prof_add_course', methods = ['POST'])
# def prof_add_course(key,prof_id):
#     response = authenticate_api_key(key)
#     if(response['response'] != '200'):
#         return jsonify(response)
#     if request.method == "POST":
#         course_name = request.form.getlist("cname")
#         section_list = request.form.getlist("slists")
        
#         course_ID = db.write_course_entry(prof_id,course_name)
#         for section_name in section_list:
#             db.write_section_entry(course_ID,section_name)
#         return jsonify({'response':'200','course_ID':course_ID})
#     return jsonify({'response':'503','message':'Internal server error'})


# '''Posts a note with the course code supplied as a request parameter'''
# @app.route('/api/<string:key>/<string:section_id>/post_note', methods=['POST'])
# def post_note(key,section_id):
#     response = authenticate_api_key(key)
#     if(response['response'] != '200'):
#         return jsonify(response)
#     #Checks for a photo upload
#     if request.method == "POST" and "photo" in request.files:
#         request.files["photo"].filename = str(hash(request.files["photo"].filename))+".jpg"
#         filename = photos.save(request.files["photo"])

#         print(request.form)
#         #TODO: FINISH UP WRITING TO THE DATABASE FOR THE PROPER ROUTING
#         db.write_note_entry(request.form["note"],filename,section_id)

#     return jsonify({'response':'200','message':'successfully written a note'})
    
        
# @app.route('/api/<string:key>/<string:prof_id>/get_notes_by_prof', methods=['GET'])
# def get_notes_by_prof(key,prof_id):
#     json_return = authenticate_api_key(key)
#     if(json_return['response'] != '200'):
#         return jsonify(json_return)
    
#     if db.prof_id_exists(prof_id):
#         return json.dumps((db.read_notes_by_prof(prof_id)))
#     return jsonify({'response':'200'})

# #TODO: FINISH THE JSON.DUMPS ON THE BOTTOM
# @app.route('/api/<string:key>/<string:course_id>/get_notes_by_course',methods= ['GET'])
# def get_notes_by_course(key,course_id):
#     json_return = authenticate_api_key(key)
#     if(json_return['response'] != '200'):
#         return jsonify(json_return)
    
#     if db.course_id_exists(course_id):
#         return json.dumps((db.read_notes_by_course(course_id)))
#     return jsonify({'response':'200'})

# @app.route('/api/<string:key>/<string:section_id>/get_notes_by_section',methods=['GET'])
# def get_notes_by_section(key,section_id):
#     json_return = authenticate_api_key(key)
#     if(json_return['response'] != '200'):
#         return jsonify(json_return)
#     if db.section_id_exists(section_id):
#         return json.dumps(db.read_notes_by_section(section_id))
#     return jsonify({'response':'200'})

#TEST ROUTE
@app.route('/api/test')
def test_route():
    return render_template("index.html")


@app.route('/<prof_id>/class')
def goClass(prof_id):
    return render_template("createclass.html")

@app.route('/<string:prof_id>/section/<string:class_id>')
def goSection(prof_id,class_id):
    return render_template("choosesection.html")

@app.route('/<prof_id>/feed')
def goFeed(prof_id):
    return render_template("landingpage.html")

@app.route('/profile')
def goProfile():
    return render_template("profile.html")

@app.route('/')
def goLogin():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True, port=8080) #TAKE OUT DEBUG IN PRODUCTION