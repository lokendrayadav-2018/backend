from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import sys
import os
import torch
from werkzeug.utils import secure_filename
from script import generateSummary
from common import extract_hindi_content
from common import read_pdf
from abstrative_summary import generate_abstractive_summary
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
app = Flask(__name__)
CORS(app)  # Enable CORS

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
app.config['UPLOAD_PATH'] = 'uploads'



# Declare these as global to make them accessible in the route handling functions
global model
global tokenizer

def load_model():
    global model
    global tokenizer
    try:
        check_pt = "csebuetnlp/mT5_multilingual_XLSum"
        print("Loading the T5 model and tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(check_pt)
        #model = AutoModelForSeq2SeqLM.from_pretrained(check_pt)
        model = torch.load("E:\checkpoint_t5.pth",map_location=torch.device('cpu'))
        print("Model and tokenizer successfully loaded.")
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        exit(1)  # Exit the application if the model cannot be loaded


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
    # summary_word  =10
    # if(data['number']):
    #     summary_word =data['number']

    if(data['type']=='1'):
        compression_ratio = 0.4
        result  = generateSummary(text,compression_ratio)
        return jsonify({
            'output': result,
            'error': "",
            'status': 200
        }) 
    elif(data['type']=='2'):
        global model
        global tokenizer
        result = generate_abstractive_summary(text,model,tokenizer)
        return jsonify({
            'output': result,
            'error': "",
            'status': 200
        })
    else:
        return jsonify({
            'output': "",
            'error': "Please Pass Correct Request",
            'status': 1005
        })


if __name__ == "__main__":
    load_model() 
    app.run(debug=True)
