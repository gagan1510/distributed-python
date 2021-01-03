import sys
from flask import Flask
from flask import render_template
from flask import request
import time
import json
from random import randint
import os
sys.path.append('.')
sys.path.append('./utils')
sys.path.append('./worker')
sys.path.append('./statics')
from task import run_job
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET'])
def root():
    """ Default route Message
    """
    return static.constants.DEFAULT_ROUTE_MESSAGE

@app.route('/_ah/health')
def default():
    """ Health status check weather flask app is running or not """
    return const.DEFAULT_HEALTH_MESSAGE

@app.route('/create_job', methods=['POST'])
def create_job():
    """
    CREATES JOB FOR A CREATE REQUEST.
    receives:
        {
            "url": "https://api.ipfy.org"
        }
    """
    try:
        # GETTING DATA
        data_for_job = {}
        input_data = request.json
        data_for_job['url'] = input_data['url']
    except:
        return json.dumps({"status": "error". "message": "please check your input."}), 500
    
    try:
        # CREATING JOB ENTRY IN MONGO. PS: MONGO ENTRY WILL ALSO BE CREATED BY THE WORKER's FRAMEWORK BUT THIS IS FOR DEV's CONVENIENCE
        job_id = utils.create_job_entry(data_for_job)
    except:
        return json.dumps({"status": "error". "message": "error while creating job entry"}), 500
    
    try:
        # QUEUE A JOB
        utils.create_job(job_id, data_for_job)
    except:
        return json.dumps({"status": "error". "message": "error while creating job"}), 500
    
    return json.dumps({"status": "error". "message": "error while creating job"}), 500

@app.route('/get_status', methods=['GET'])
def get_status():
    """
        GET THE STATUS OF CURRENT/ALREADY CREATED JOB
    """
    job_id = request.args['job_id']
    result = matching_utils.get_job_result(job_id)
    return json.dumps(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)