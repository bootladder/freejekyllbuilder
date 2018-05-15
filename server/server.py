from __future__ import print_function
import sys
import simplejson as json
import flask
from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
import subprocess
from subprocess import Popen, PIPE, STDOUT

app = Flask(__name__)
CORS(app)

boundarypath = "/opt/boundary/"
audiofilespath = "/opt/files/"

@app.route('/upload/<path:path>', methods = ['POST'])
def upload_file(path):
    flaskprint('\n\nUpload:  ' + path )
    f = request.files.values()[0]
    #pathtofile = audiofilespath+secure_filename(f.filename)
    pathtofile = audiofilespath+path
    f.save(pathtofile)
    flaskprint('[route] Received a File, saved blob to'+pathtofile+'\n')

    # Execute Use Case 
    p = Popen(['sh',boundarypath+'/'+'upload',path], 
                      stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data,stderr_data  = p.communicate(input=pathtofile+'\n')
    flaskprint('[UseCase Output] '+stdout_data)

    # Check Exit Code of the boundary
    if p.returncode != 0:
        flaskprint("[UseCase Return Code != 0]: /"
                      +'upload'+": Failed, stderr: "+stderr_data)
        return flask.Response('The Use Case Failed, Brah', status=500)

    return "response!"

@app.route('/download/<path:path>')
def send_js(path):
    return send_from_directory(audiofilespath, path+'.zip',
        as_attachment=True,attachment_filename=path+'.zip')

@app.route('/metaselfdeploy',methods = ['POST','GET'])
def metaselfdeploy():
    p = Popen(['sh',boundarypath+'/'+'metaselfdeploy'], 
                      stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data,stderr_data  = p.communicate(input='\n')
    flaskprint('[UseCase Output] '+stdout_data)

    # Check Exit Code of the boundary
    if p.returncode != 0:
        flaskprint("[UseCase Return Code != 0]: /"
                      +'upload'+": Failed, stderr: "+stderr_data)
        return flask.Response('The Use Case Failed, Brah', status=500)
    return 'deployed!'
		
@app.route('/status/<path:path>',methods = ['POST'])
def audiomessageapi_update():
    resp = common_route_handler(request, 'update')
    return resp

@app.route('/')
def hello_world():
    return send_from_directory('.', 'index.html')

# Grabs stuff out of the HTTP Request
# Executes Use Case, Gives Request Model to it
def common_route_handler(request, usecase):

    flaskprint('\n\n\n\n\n\nFlask Route Handler:  '+usecase+'\n')

    # Handle a File Upload
    # Save the Audio Blob to filesystem
    if 'file' in request.files:
        f = request.files['file']
        pathtofile = audiofilespath+secure_filename(f.filename)
        f.save(pathtofile)
        flaskprint('[route] Received a File, saved blob to'+pathtofile+'\n')
    
    # Request must have a requestmodel
    if 'requestmodel' not in request.form:
        flaskprint('[route] AJAX attempt with no requestmodel \n')
        return flask.Response('No requestmodel', status=500)

    # Validate we get a JSON
    json_str = request.form['requestmodel'].encode('utf-8')
    json_dict = json.loads(json_str)
    flaskprint('[RequestModel, Parsed]: ')
    flaskprint(json_dict)

    # If there was a File Upload, include the Path in the RequestModel
    if 'file' in request.files:
        json_dict['pathtofile'] = pathtofile 
        json_str = json.dumps(json_dict)

    # Execute Use Case and Pass the JSON to it
    p = Popen([boundarypath+'/'+usecase], 
                      stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data,stderr_data  = p.communicate(input=json_str+'\n')
    flaskprint('[UseCase Output] '+stdout_data)

    # Check Exit Code of the boundary
    if p.returncode != 0:
        flaskprint("[UseCase Return Code != 0]: /"
                      +usecase+": Failed, stderr: "+stderr_data)
        return flask.Response('The Use Case Failed, Brah', status=500)
        

    # Send response
    response_text = stdout_data
    resp = flask.Response(response_text)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
	
def flaskprint(stupid):
    print(stupid, file=sys.stderr)

if __name__ == '__main__':
		context = ('cert.crt', 'key.key')
		app.run(debug = True,host='0.0.0.0', threaded=True, port=9004)
#ssl_context=context, 



