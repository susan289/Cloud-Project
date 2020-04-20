#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
import requests
import hashlib, binascii, os
import mysql.connector

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):

    
    if username == 'susan':
        return 'python'
    elif username == 'admin':
        return 'admin'
    else:
        mydb = mysql.connector.connect(
        host="localhost",
        user="developer",
        passwd="developer",
        database="mydb"
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT username, password FROM app_users")
        myresult = mycursor.fetchall()
        for username in myresult:
          return username 
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

wparameters = [
    {
        'id': 1,
        'title': u'Temparature',
        'description': u'Immediete Temparature,Intervalues Temparature', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Humidity',
        'description': u'Relative Humidity,Absolute Humidity', 
        'done': False
    }
]

def make_public_wparameter(task):
    new_wparameter = {}
    for field in task:
        if field == 'id':
            new_wparameter['uri'] = url_for('get_wparameter', task_id = task['id'], _external = True)
        else:
            new_wparameter[field] = task[field]
    return new_wparameter
    
@app.route('/weather/api/v1.0/wparameters', methods = ['GET'])
@auth.login_required
def get_wparameters():
    return jsonify( { 'wparameters': map(make_public_wparameter, wparameters) } )

@app.route('/weather/api/v1.0/wparameters/<int:task_id>', methods = ['GET'])
@auth.login_required
def get_wparameter(task_id):
    task = filter(lambda t: t['id'] == task_id, wparameters)
    if len(task) == 0:
        abort(404)
    return jsonify( { 'task': make_public_wparameter(task[0]) } )

@app.route('/weather/api/v1.0/wparameters', methods = ['POST'])
@auth.login_required
def create_wparameter():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': wparameters[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    wparameters.append(task)
    return jsonify( { 'task': make_public_wparameter(task) } ), 201

@app.route('/weather/api/v1.0/wparameters/<int:task_id>', methods = ['PUT'])
@auth.login_required
def update_wparameter(task_id):
    task = filter(lambda t: t['id'] == task_id, wparameters)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify( { 'task': make_public_wparameter(task[0]) } )
    
@app.route('/weather/api/v1.0/wparameters/<int:task_id>', methods = ['DELETE'])
@auth.login_required
def delete_wparameter(task_id):
    task = filter(lambda t: t['id'] == task_id, wparameters)
    if len(task) == 0:
        abort(404)
    wparameters.remove(task[0])
    return jsonify( { 'result': True } )

@app.route('/weather/api/v1.0/city')
@auth.login_required
def search_city():
    API_KEY = '183fb3e8c765b0233b773d8d0d4812c3'  # initialize your key here
    city = request.args.get('name')  # city name passed as argument
    
    # call API and convert response into Python dictionary
    #url = 'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
    url = 'http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=183fb3e8c765b0233b773d8d0d4812c3'
    response = requests.get(url).json()
    
    # error like unknown city name, inavalid api key
    if response.get('cod') != 200:
        message = response.get('message', '')
        return 'Error getting temperature for {city.title()}. Error message = {message}'
    
    # get current temperature and convert it into Celsius
    current_temperature = response.get('main', {}).get('temp')
    if current_temperature:
        current_temperature_celsius = round(current_temperature - 273.15, 2)
        #return 'Current temperature of {city.title()} is {current_temperature_celsius} &#8451;'
        return response
    else:
        return 'Error getting temperature for {city.title()}'
 
@app.route('/weather/api/v1.0/storehashpassword')
def store_password():
    username=request.args.get('user')
    hash_object = hashlib.md5(username)
    hashp=hash_object.hexdigest()
    mydb = mysql.connector.connect(
    host="localhost",
    user="developer",
    passwd="developer",
    database="mydb"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO app_users (username,password) VALUES (%s,%s)"
    val = (username, hashp)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")
    return 'The hashpasswrod of user '+username+' is '+hash_object.hexdigest()+ ' <br/>successfuly stored in database'
    
    

@app.route('/weather/api/v1.0')
def index():
    return '<p><span style="color: #ff0000;">Welcome to weather API</span></p><p><strong><span style="color: #000000;">List of End Points:</span></strong></p><p>&nbsp;</p><table style="height: 120px; width: 792px; border-color: green;" border="1"><tbody><tr><td style="width: 80px;"><strong><span style="background-color: #ffffff;">Method</span></strong></td><td style="width: 359px;"><strong><span style="background-color: #ffffff;">URL</span></strong></td><td style="width: 84.8px;"><strong><span style="background-color: #ffffff;">Parameter</span></strong></td><td style="width: 161.2px;"><strong><span style="background-color: #ffffff;">Description</span></strong></td></tr><tr><td style="width: 80px;">GET</td><td style="width: 359px;"><a href="http://localhost:5000/weather/api/v1.0/storehashpassword?user=demo12">/weather/api/v1.0/storehashpassword</a></td><td style="width: 84.8px;">user</td><td style="width: 161.2px;">Create a new user with MD5 based hash password</td></tr><tr><td style="width: 80px;">GET</td><td style="width: 359px;"><a href="http://localhost:5000/weather/api/v1.0/city?name=kolkata">/weather/api/v1.0/city</a></td><td style="width: 84.8px;">name</td><td style="width: 161.2px;">Fetches Weather Information For a City</td></tr><tr><td style="width: 80px;">GET</td><td style="width: 359px;"><a href="http://localhost:5000/weather/api/v1.0/wparameters">/weather/api/v1.0/wparameters</a></td><td style="width: 84.8px;">&nbsp;</td><td style="width: 161.2px;">Get All Weather Parameters</td></tr><tr><td style="width: 80px;">GET</td><td style="width: 359px;"><a href="http://localhost:5000/weather/api/v1.0/wparameters/1">/weather/api/v1.0/wparameters&lt;int:id&gt;</a></td><td style="width: 84.8px;">parameter id</td><td style="width: 161.2px;">Get Specific Parameter</td></tr><tr><td style="width: 80px;">POST</td><td style="width: 359px;"><a href="http://localhost:5000/weather/api/v1.0/wparameters">/weather/api/v1.0/wparameters/</a></td><td style="width: 84.8px;">{"title":"Rain Forcsats"}</td><td style="width: 161.2px;">Post new Weather Parameter</td></tr><tr><td style="width: 80px;">PUT</td><td style="width: 359px;"><a href="http://localhost:5000/weather/api/v1.0/wparameters/3">/weather/api/v1.0/wparameters&lt;int:id&gt;</a></td><td style="width: 84.8px;">{"description":"To Put Rain Forecasts"}</td><td style="width: 161.2px;">Put New Parameters</td></tr><tr><td style="width: 80px;">DELETE</td><td style="width: 359px;"><a href="http://localhost:5000/weather/api/v1.0/wparameters/3">/weather/api/v1.0/wparameters&lt;int:id&gt;</a>&nbsp;</td><td style="width: 84.8px;">&nbsp;{"id":"1"}</td><td style="width: 161.2px;">Delete a parameters</td></tr></tbody></table><p>&nbsp;</p>'   
    
    
if __name__ == '__main__':
    app.run(debug = True)
