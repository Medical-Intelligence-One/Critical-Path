from operator import imod
from flask_cors import CORS
from flask import Flask, redirect , url_for, render_template, request, jsonify
from flask.wrappers import Response
from numpy import roots
import fetchData
from flask import request, jsonify, Response
import json
import requests
import pandas as pd

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>MI-1 Sherlock</h1>
<p>A prototype API for Medical Intelligence One's cognitive computing platform.</p>'''

@app.route('/api/autocomplete_rareDz_findings', methods=['GET', 'POST'])
def api_autocomplete_rareDz_findings(): 
    data = request.data
    parsed = json.loads(data)
    startingtext = parsed['startsWith'][0]['startsWith']
    
    apidata = fetchData.autocomplete_rareDz_findings(startingtext)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    result_data = jsonify(parsed)
    return result_data

@app.route('/api/rareDiseaseSearchPosNeg', methods=['GET', 'POST'])
def api_rareDiseaseSearchPosNeg(): 
    pproblem = request.data
    parsed = json.loads(pproblem)
    Matched_Findings=[]
    Negative_Matched_Findings=[]
    for item in parsed['Matched_Findings']:
        Matched_Findings.append(item['CUI'])
    if parsed['Negative_Matched_Findings'] != []:
        for item in parsed['Negative_Matched_Findings']:
            Negative_Matched_Findings.append(item['CUI'])
    
    apidata = fetchData.rareDiseaseSearchPosNeg(Matched_Findings, Negative_Matched_Findings)

    # Handle empty results
    if(apidata.empty):
        return jsonify([])
    else:
        result = apidata.to_json(orient="records")
        parsed = json.loads(result) 
        result_data = jsonify(parsed)
    # result_data.headers.add("Access-Control-Allow-Origin", "*")
        return result_data