from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
import numpy as np
import json
import math

app=Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def preprocessing(s):
    i=0
    a=""
    for i in range(len(s)):
        if (ord(s[i]) >= ord('A') and
            ord(s[i]) <= ord('Z') or 
            ord(s[i]) >= ord('a') and 
            ord(s[i]) <= ord('z') or
            ord(s[i]) == ord(' ')):
            a += s[i] 
    a=' '.join(a.split())
    a=a.lower()
    return a

def compute_likelihood(test_X, classes,model,d):
    likelihood=0
    word=test_X.split()
    
    for i in word:
        count=0
        frequency=(model[classes])
        if i in frequency:
            count=model[classes][i]
        likelihood+=np.log((count+1)/d[classes])
        
    return likelihood

def predict_target_values(test_X,final_model):
    model=final_model["model"]
    prior_prob=final_model["prior_prob"]
    word_count=final_model["word_count"]
    classes=final_model["classes"]
    classes=[str(val) for val in classes]
    n=1
    pred=np.zeros((n,1))
    for i in range(n):
        best_p=-math.inf
        best_c=-1
        for c in classes:
            p=compute_likelihood(preprocessing(test_X),c,model,word_count)+np.log(prior_prob[c])
            if p>best_p:
                best_p=p
                best_c=c
        pred[i][0]=best_c
    return pred

def import_data_and_model( model_file_path):
    
    with open(model_file_path,'r') as json_file:
        model=json.load(json_file)
    
    return model

def predict(test_data):
    model = import_data_and_model("./model_file.json")
    pred_Y = predict_target_values(test_data, model)
    return pred_Y

@app.route("/predict/",methods=['POST'])

def hello():
    file=request.json
    prediction=predict(file["data"])
    ans=prediction[0][0]
    return jsonify({"prediction":str(ans)})



if __name__=="__main__":
    app.run(debug=True)