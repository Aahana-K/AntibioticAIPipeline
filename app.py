#importing libraries
import numpy as np
import flask
import pickle
import joblib
from flask import Flask, request, jsonify
import os
import matplotlib.pyplot as plt

#creating instance of the class
import pandas as pd
import numpy as np
from flask_cors import CORS
from lime.lime_tabular import LimeTabularExplainer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from math import sqrt
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder

from torch.utils.data import DataLoader, TensorDataset
import torch.nn.functional as F

import json
from torch.autograd import Variable
import joblib
import os


organtibioticAI = joblib.load('antibioticAIstage1.joblib')
outantibioticAI = joblib.load('antibioticAIstage2.joblib')

pAth = os.path.dirname(os.path.abspath(__file__))
cAge = joblib.load(os.path.join(pAth,'age.pkl'))
cAntibiotic = joblib.load(os.path.join(pAth,'antibiotic.pkl'))
cCulture = joblib.load(os.path.join(pAth,'culture.pkl'))
cOrganism = joblib.load(os.path.join(pAth,'organism.pkl'))

'''
'''


app=Flask(__name__)
CORS(app)
def home():
    return '2 stage Ai pipeline predicting bacterial infections and treatment outcomes'
@app.route('/predict',methods=['POST'])
def predict():
    try:
        antibiotics = ['Levofloxacin', 'Nitrofurantoin', 'Amikacin' ,'Trimethoprim/Sulfamethoxazole' ,'Tobramycin', 'Gentamicin' ,'Ampicillin' ,'Ciprofloxacin' ,'Cefazolin' ,'Piperacillin/Tazobactam' ,'Ceftriaxone' ,'Ceftazidime' ,'Meropenem' ,'Ertapenem' ,'Tetracycline' ,'Amoxicillin/Clavulanic Acid', 'Cefoxitin', 'Cefepime', 'Aztreonam' ,'Moxifloxacin' ,'Cefuroxime' ,'Imipenem' ,'Tigecycline', 'Ampicillin/Sulbactam' ,'Linezolid' ,'Daptomycin', 'Penicillin', 'Vancomycin', 'Cefotaxime', 'Cefotetan', 'Clarithromycin', 'Doxycycline', 'Clindamycin', 'Oxacillin', 'Erythromycin', 'Ceftaroline' ,'Ticarcillin', 'Piperacillin', 'Streptomycin', 'Imipenem/Ebactam', 'Ceftolozane/Tazobactam', 'Fosfomycin', 'Metronidazole', 'Doripenem', 'Ceftazidime/Avibactam', 'Quinupristin/Dalfopristin', 'Colistin', 'Minocycline', 'Ticacarcillin/Clavulanic Acid', 'Cephalexin/Cephalothin', 'Cefiderocol' ,'Meropenem/Vaborbactam' ,'Cefpodoxime' ,'Chloramphenicol', 'Amoxicillin/ClavulanicAcid' ,'Ticacarcillin/ClavulanicAcid']

        pulledData=request.get_json()
        print("Raw received data:", pulledData)  # check if data arrives at all

        data = pd.DataFrame([pulledData['userInputs']])
        print("DataFrame created:", data) 
        
        print(pulledData['userInputs'])
        ageVal = int(data['age'].iloc[0])
        print("Age value:", ageVal)
        if ageVal <= 24:
            data.loc[0,'age'] = '18-24 years'
        elif ageVal > 24 and ageVal <= 34:
            data.loc[0,'age'] = '25-34 years'
        elif ageVal >= 35 and ageVal <= 44:
            data.loc[0,'age'] = '35-44 years'
        elif ageVal >= 45 and ageVal <= 54:
            data.loc[0,'age'] = '45-54 years'
        elif ageVal >= 55 and ageVal <= 64:
            data.loc[0,'age'] = '55-64 years'
        elif ageVal >= 65 and ageVal <= 74:
            data.loc[0,'age'] = '65-74 years'
        elif ageVal >= 75 and ageVal <= 84:
            data.loc[0,'age'] = '75-84 years'
        elif ageVal >= 85 and ageVal <= 89:
            data.loc[0,'age'] = '85-89 years'
        elif ageVal >= 90:
            data.loc[0,'age'] = 'above 90'


        tAge = cAge.transform(data[['age']])
        tCulture = cCulture.transform(data[['culture_description']])


        ageDf = pd.DataFrame(tAge,columns=['age'],index=data.index)
        cultureDf = pd.DataFrame(tCulture,columns=['culture_description'],index=data.index)
        print("Model expects columns:", organtibioticAI.feature_names_in_)


        dataOrganism = pd.concat([data.drop(columns=['age','culture_description']),ageDf,cultureDf],axis=1)
        dataOrganism = dataOrganism.apply(pd.to_numeric)
        print("DataFrame dtypes:", dataOrganism.dtypes)
        '''
        organismPrediction = organtibioticAI.predict(dataOrganism)
        print("Organism prediction:", organismPrediction)
        dataOrganism['organism'] = organismPrediction
        dataOutcomes = dataOrganism.copy()
        dataOrganism = dataOrganism.drop('organism',axis=1)
        
        susceptibleAntibiotics = {}
        intermediateAntibiotics = {}
        resistantAntibiotics = {}
'''
        organismPrediction = organtibioticAI.predict(dataOrganism)
        print("Organism prediction:", organismPrediction)

        dataOrganism['organism'] = organismPrediction
        print("Added organism column")

        dataOutcomes = dataOrganism.copy()
        print("Copied to dataOutcomes")

        dataOrganism = dataOrganism.drop('organism', axis=1)
        print("Dropped organism from dataOrganism")

        susceptibleAntibiotics = {}
        intermediateAntibiotics = {}
        resistantAntibiotics = {}
        print("Dicts created, starting loop")
        for antibiotic in antibiotics:
            dataOutcomesA = dataOutcomes.copy()
            tAntibiotic = cAntibiotic.transform([[antibiotic]])[0][0]
            dataOutcomesA['antibiotic'] = tAntibiotic

            confidenceProbs = outantibioticAI.predict_proba(dataOutcomesA)
            confidence = confidenceProbs.max()
            classIndex= confidenceProbs.argmax()
            outcomePredicted = outantibioticAI.classes_[classIndex]
            
            if outcomePredicted == 'Susceptible':
                susceptibleAntibiotics[antibiotic] = confidence
            elif outcomePredicted == 'Resistant':
                resistantAntibiotics[antibiotic] = confidence
            else:
                intermediateAntibiotics[antibiotic] = confidence
        dataOutcomesA = dataOutcomesA.drop('antibiotic',axis=1)
        if len(susceptibleAntibiotics) >= 1:
            antibioticc = max(susceptibleAntibiotics, key=susceptibleAntibiotics.get)
            dataExplain = dataOutcomes.copy()
            tAntibioticc = cAntibiotic.transform([[antibioticc]])[0][0]
            dataExplain['antibiotic'] = tAntibioticc
            dataExplain = dataExplain[outantibioticAI.feature_names_in_]
            samplee = dataExplain.iloc[0].values
            
        
            return jsonify({
                    'predicted bacterium': cOrganism.inverse_transform([[organismPrediction[0]]])[0][0],
                    'antibiotic': max(susceptibleAntibiotics, key=susceptibleAntibiotics.get),
                    'outcome': 'susceptible',
                    'antibioticConfidenceScore': float(max(susceptibleAntibiotics.values()))})
        elif len(intermediateAntibiotics) >=1:
            return jsonify({
        'predicted bacterium': cOrganism.inverse_transform([[organismPrediction[0]]])[0][0],
        'antibiotic': max(intermediateAntibiotics, key=intermediateAntibiotics.get),
        'outcome': 'intermediate',
        'antibioticConfidenceScore': float(max(intermediateAntibiotics.values())),
        })
        else:
            return jsonify({
        'predicted bacterium': cOrganism.inverse_transform([[organismPrediction[0]]])[0][0],
        'antibiotic': min(resistantAntibiotics, key=resistantAntibiotics.get),
        'outcome': 'resistant',
        'antibioticConfidenceScore': float(min(resistantAntibiotics.values()))})
    except Exception as e:
        import traceback
        print("FULL ERROR:", traceback.format_exc())
        return jsonify({'error': str(e)}), 400
    
if __name__ == '__main__':
    app.run(debug=True)