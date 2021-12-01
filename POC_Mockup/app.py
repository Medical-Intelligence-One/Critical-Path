import flask
from flask.wrappers import Response
from numpy import roots
import fetchData
from flask import request, jsonify
import json
import requests
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/PotentialComorbidities', methods=['GET'])
def api_PotentialComorbidities(): 
    pproblem = request.data
    parsed = json.loads(pproblem)
    cui_prob_list=[]
    for item in parsed['CUIs']:
        cui_prob_list.append(item['CUI'])
    
    apidata = fetchData.PotentialComorbidities(cui_prob_list)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)

@app.route('/api/LikelyAbnormalLabs', methods=['GET'])
def api_LikelyAbnormalLabs(): 
    pproblem = request.data
    parsed = json.loads(pproblem)
    cui_prob_list=[]
    for item in parsed['CUIs']:
        cui_prob_list.append(item['CUI'])
    
    apidata = fetchData.LikelyAbnormalLabs(cui_prob_list)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)

@app.route('/api/LikelyPrescriptions', methods=['GET'])
def api_LikelyPrescriptions(): 
    pproblem = request.data
    parsed = json.loads(pproblem)
    cui_prob_list=[]
    for item in parsed['CUIs']:
        cui_prob_list.append(item['CUI'])
    
    apidata = fetchData.LikelyPrescriptions(cui_prob_list)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)

if __name__ == '__main__':
    app.debug = True
    app.run(host="76.251.77.235", port=5000) #host="0.0.0.0" will make the page accessable
                            #by going to http://[ip]:5000/ on any computer in 
                            #the network.