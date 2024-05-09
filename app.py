from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import sys
app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/runscript', methods=['POST'])
def run_script():
    # You can access the sent data here, if needed
    data  = request.form
    #  find appropriate text for classification
    text = "";
    if(data['source']==2):
        text = data['text']
    elif(data['source']==3):
        text = data['text']
    else:
        text = data['text']

    
    if(data['type']=='1'):
        result = subprocess.run(['python', 'script.py', '--text', text], capture_output=True, text=True)
        response_output = result.stdout
        response_error = result.stderr
        return jsonify({
            'output': response_output,
            'error': response_error,
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
