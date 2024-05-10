from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import sys
from script import generateSummary
from common import extract_hindi_content
from common import read_pdf
app = Flask(__name__)
CORS(app)  # Enable CORS

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
        file="example.pdf"
        text = read_pdf(file)
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
