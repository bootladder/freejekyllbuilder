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
app.config['MAX_CONTENT_PATH'] = 1024*1024*128 #to accept large zip files

boundarypath = "/opt/boundary/"
filestoragepath = "/opt/files/"

# Receives a zip file containing the site source
# Save the file, then build the site with jekyll
@app.route('/upload/<path:path>', methods = ['POST'])
def upload_file(path):
    flaskprint('\n\nUpload:  ' + path )
    if 'file' not in request.files:
      return "no file in there"

    flaskprint('\n\nrequest.files:  ' + request.files['file'].filename )

    f = request.files['file']
    pathtofile = filestoragepath+path
    f.save(pathtofile)
    flaskprint('[route] Received a File, saved blob to'+pathtofile+'\n')

    # Execute Use Case
    p = Popen(['sh',boundarypath+'/'+'upload',path],
                      stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data,stderr_data  = p.communicate(input=pathtofile+'\n')
    flaskprint('[UseCase Output] '+stdout_data)

    # Check Exit Code
    if p.returncode != 0:
        flaskprint("[UseCase Return Code != 0]: /"
                      +'upload'+": Failed, stderr: "+stderr_data)
        return flask.Response('The Use Case Failed, Brah', status=500)

    return "response!"

# User Downloads the built site here
@app.route('/download/<path:path>')
def send_js(path):
    return send_from_directory(filestoragepath, path+'.zip',
        as_attachment=True,attachment_filename=path+'.zip')


# Assuming the homepage of freejekyllbuilder.com is hosted on the same host,
# This server.py can conveniently deploy the site to the web root.
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

# Assuming the homepage of freejekyllbuilder.com is hosted on the same host,
# Serve the static site
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_worldz(path):
    flaskprint('path: ' + path)
    if path == '':
      return send_from_directory('/opt/webroot/', 'index.html')

    return send_from_directory('/opt/webroot/', path)

# For debugging... print() doesn't print to flask console for some reason...
def flaskprint(stupid):
    print(stupid, file=sys.stderr)

# Run the flask server.
# NOTE the commented out SSL stuff.
if __name__ == '__main__':
		#context = ('cert.crt', 'key.key')
		app.run(debug = True,host='0.0.0.0', threaded=True,
    #ssl_context=context,
    port=9004)




