# importing regex, pandas, sqlite3, and flask
import re
from flask import Flask, jsonify
import pandas as pd
import sqlite3

import os
from os.path import join, dirname, realpath

# importing clean_slang function from cleansing_function.py
from cleansing_function import clean_slang, clean_abusive

# importing request, Swagger, LazyString, and LaztJSONEncoder, and swag_from
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from

# creating the app & turning on debug mode
app = Flask(__name__)
app.config["DEBUG"] = True

# defining folder path
UPLOAD_FOLDER = 'static/uploaded_files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# encoding dictionary to json
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda: '2.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    # assigning to the host
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
# activating the swagger, passing the swagger_template & swagger_config to the Swagger
swagger = Swagger(app, template=swagger_template,config=swagger_config)

# creating the end-point
@app.route('/', methods=['GET'])
def home():
    return '<a href="http://127.0.0.1:5000/docs">Go to Swagger UI docs</a>'

# endpoint to upload csv file
@swag_from("docs/upload_file.yml", methods=['POST'])
@app.route("/upload_files", methods=['POST'])
def upload_files():
      # getting the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # setting up the file path
        uploaded_file.save(file_path)
        # here we expect csv file to be read
        df = pd.read_csv(file_path, encoding='latin-1')
    return str(df)

# endpoint to text cleansing
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    
    # creating connection to sqlite database and assigning the table into variable
    connection = sqlite3.connect('data/slang.db')
    slang_df = pd.read_sql('''SELECT * FROM slangwords;''', connection)
    connection.close()

    # assigning abusive.csv file to a variable
    abusive_df = pd.read_csv('data/abusive.csv')

    # getting data from the form
    text = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': "Original Text",
        'data': re.sub(r'[\W]', ' ', clean_abusive(clean_slang(text, slang_df), abusive_df))
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run(debug=True)