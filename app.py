from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import sys
import os
from werkzeug.utils import secure_filename
from script import generateSummary
from common import extract_hindi_content
from common import read_pdf
app = Flask(__name__)
CORS(app)  # Enable CORS

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/runscript', methods=['POST'])
def run_script():
    # You can access the sent data here, if needed
    data  = request.form
    #  find appropriate text for classification
    text = "";
    if(data['source']=="2"):
        temp = data['url']
        text = extract_hindi_content(temp)
    elif(data['source']=="3"):
        #file = data['file']

        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        if filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        text = read_pdf(file_path)
    else:
        text = data['text']
    
    if(data['type']=='1'):
        result  = generateSummary(text)
        return jsonify({
            'output': result,
            'error': "",
            'status': 200
        }) 
    elif(data['type']=='2'):
        return jsonify({
            'output': data,
            'error': "HII",
            'status': 200
        })
    else:
        return jsonify({
            'output': "",
            'error': "Please Pass Correct Request",
            'status': 1005
        })


if __name__ == "__main__":
    app.run(debug=True)
