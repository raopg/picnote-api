## RESTful API for picNote  
## A collaborative note-taking app using Python Flask, Flask-S3 

Base URL = https://picnote.io/api/*API_KEY*/

###Endpoints

#### Professor Login
POST /login
params = username:str, password:str
return  = prof_id

#### Add Course(Professor Only)
POST /prof_add_course
params = hashed:int //hashed = prof_id
return = course_id:int

#### Post Note(Student Only)
POST /post_note
params = course_id:int
return = None

#### Get Notes by ID
GET /get_notes
params = hahsed:int // Depending on whether is it a professor ID , course ID or a section ID, returns notes categorized by that ID
return = list(JSON)


