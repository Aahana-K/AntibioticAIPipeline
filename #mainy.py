#main.py
# prep dataset
print("started running")
import pandas as pd
import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import sklearn
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
'''
alrExists = []
comorbidityWeights = {
    "charlsonCondition_myocardialInfraction":1,
    #heart attack: when blood flow to a part of the heart muscle is blocked causing that heart tissue to die from lack oxygen
    "charlsonCondition_congestiveHeartFailure":1,
    #heart failure heart cant pump enough blood for body's need
    "charlsonCondition_peripheralVascularDisease":1,
    #narrowed arteries reduce blood flow usually caused by plaque build up atheroscelerosis
    "charlsonCondition_cerebrovascularDisease":1,
    #leads to strokes brainbleeds cuz affects blood flow to brain
    "charlsonCondition_chronicPulmonaryDisease":1,
    #lung diseases affecting lungs airway; asthma, bronchitis, emphysema, cystic fibrosis, pulmonary fibrosis
    "charlsonCondition_rheumaticDisease":1,
    #musculoskeletal and autoimmune conditions: rheumatoid arthrisis, lupus, gou, osteoarthritis
    #painful sores in stomach lining or upper smal intestine
    "charlsonCondition_mildLiverDisease":1,
    "charlsonCondition_diabetesnoChronicComplication":1,
    "charlsonCondition_diabeteswEndOrganDamage":2,
    "charlsonCondition_renalDisease":2,
    #kidneys damaged cantfitler waste
    "charlsonCondition_anymalignancy/lymphoma/leukemia":2,
    #blood, bone and lymphatic systme cancers from abnormal white blood cell growth
    "charlsonCondition_moderateoSevereLiverDisease":3,
    "charlsonCondition_metastaticSolidTumour":6,
    "charlsonCondition_hematologicDisease":1
}
bacterialInfectionTypes = {
    'TrueBacteriaCocci':[],
    'TrueBacteriaBacilli':['KLEBSIELLA PNEUMONIAE'],
    'Actinomycetes':[],
    'Spirochaetes':[],
    'Mycoplasmas':[],
    'Rickettsia':[],
    'Chlamydiae':[],
}
'''


pAth = os.path.dirname(os.path.abspath(__file__))
pathh = os.path.dirname(os.path.abspath(__file__))

#data=pd.read_csv(os.path.join(pAth,'antibioticStage2Data.csv'))
#ageData=pd.read_csv(os.path.join(pAth,'microbiology_cultures_demographics (1).csv'),dtype={'age':str},low_memory=False)
data = pd.read_csv(os.path.join(pAth,'antibioticAIinclusive.csv'))



data = data.replace('',np.nan)
data = data.dropna()


data.to_csv('antibioticAIinclusivee.csv',index=False)
'''
ageKeys = ageData.set_index(['anon_id','pat_enc_csn_id_coded','order_proc_id_coded'])['age'].to_dict()

data['age'] = data['age'].replace([0,'0','Null'],np.nan)
ageData['age'] = ageData['age'].replace([0,'0','Null'],np.nan)

merged = data.merge(
    ageData[['anon_id','pat_enc_csn_id_coded','order_proc_id_coded','age']],
    on=['anon_id','pat_enc_csn_id_coded','order_proc_id_coded'],
    how='left',
    suffixes=('','_fromAge')
)
#bigData=pd.read_csv(os.path.join(pAth,'proDemoComoTHREE.csv'))
#data[].replace('Null',np.nan,inplace=True)

merged['age']=merged['age'].fillna(merged['age_fromAge'])
merged =merged.drop(columns=['age_fromAge'])

merged.to_csv('testingtesting.csv',index=False)



data.drop('ordering_mode',axis=1,inplace=True)
data.drop('order_time_jittered_utc',axis=1,inplace=True)
bigData.drop('gender',axis=1,inplace=True)
bigData.drop('order_time_jittered_utc',axis=1,inplace=True)
grouped = pd.merge(bigData,data, on = ['anon_id','pat_enc_csn_id_coded','order_proc_id_coded'], how = 'outer')
grouped.replace(np.nan,0,inplace=True)

grouped['age'] = grouped['age'].replace([0,'Null',''],np.nan)
grouped = grouped.dropna()
'''
#data.to_csv('antibioticStage2Data.csv',index=False)

'''
hotProcedures = OneHotEncoder(sparse_output=False)
tProcedures = hotProcedures.fit_transform(data[['procedure_description']])

colProcedure = pd.DataFrame(tProcedures, columns = hotProcedures.get_feature_names_out())


data = pd.concat([data.drop(columns = ['procedure_description']),colProcedure],axis=1)

procedures = ['procedure_description_cvc','procedure_description_dialysis','procedure_description_mechvent','procedure_description_parenteral_nutrition','procedure_description_surgical_procedure','procedure_description_urethral_catheter']
#data.to_csv('testingProcedures.csv',index=False)

for procedure in procedures:
    data[procedure] = data[procedure] * data['procedure_time_to_culturetime']

data.drop('procedure_time_to_culturetime',axis=1, inplace =True)
data.drop('order_time_jittered_utc',axis=1,inplace=True)

grouped = pd.merge(bigDataset,data, on = ['anon_id','pat_enc_csn_id_coded','order_proc_id_coded'], how = 'outer')
grouped.replace(np.nan,0,inplace=True)
grouped.to_csv('proDemoComoTHREE.csv',index=False)






demoData = pd.read_csv(os.path.join(pathh,'microbiology_cultures_demographics.csv'))

grouped = pd.merge(data,demoData, on = ['anon_id','pat_enc_csn_id_coded','order_proc_id_coded'], how = 'outer')
conditions = ['charlsonCondition_anymalignancy/lymphoma/leukemia','charlsonCondition_cerebrovascularDisease','charlsonCondition_chronicPulmonaryDisease','charlsonCondition_congestiveHeartFailure','charlsonCondition_diabetesnoChronicComplication','charlsonCondition_diabeteswEndOrganDamage','charlsonCondition_hematologicDisease','charlsonCondition_metastaticSolidTumour','charlsonCondition_mildLiverDisease','charlsonCondition_moderateoSevereLiverDisease','charlsonCondition_myocardialInfraction','charlsonCondition_peripheralVascularDisease','charlsonCondition_renalDisease','charlsonCondition_rheumaticDisease','charlsonIndex']
for condition in conditions:
    grouped[condition]=grouped[condition].replace(np.nan,0)


grouped.to_csv('antibioticsAIdataset.csv',index=False)

#comorbidityGender 
#ENCODING COMOBORITIES CODE VERY IMPORTANT DO NOT DELETEEEEE

data.drop('charlsonCondition', axis = 'columns',inplace=True)
hotcols = list(comorbidityWeights.keys())

data= data.groupby(['anon_id','pat_enc_csn_id_coded','order_proc_id_coded','order_time_jittered_utc'],as_index=False)[['charlsonCondition_anymalignancy/lymphoma/leukemia','charlsonCondition_cerebrovascularDisease','charlsonCondition_chronicPulmonaryDisease','charlsonCondition_congestiveHeartFailure','charlsonCondition_diabetesnoChronicComplication','charlsonCondition_diabeteswEndOrganDamage','charlsonCondition_hematologicDisease','charlsonCondition_metastaticSolidTumour','charlsonCondition_mildLiverDisease','charlsonCondition_moderateoSevereLiverDisease','charlsonCondition_myocardialInfraction','charlsonCondition_peripheralVascularDisease','charlsonCondition_renalDisease','charlsonCondition_rheumaticDisease']].max()
for col, we in comorbidityWeights.items():
    data[col] = data[col] * we
data['charlsonIndex'] = data[list(comorbidityWeights.keys())].sum(axis=1)
data.to_csv("comoborities.csv",index=False)

#data.to_csv("jstocheck.csv", index=False)


print(data.shape)
for co in data.columns:
    data[co] = pd.to_numeric(data[co],errors='coerce')

numcols = data.select_dtypes(include=["number"]).columns
data = data.replace("Null",np.nan)
data[numcols] = data[numcols].fillna(data[numcols].median())

data.to_csv("fullmicrbioculturesLABS.csv", index=False)



comorbidityWeights = {
    "myocardialInfraction":1,
    #heart attack: when blood flow to a part of the heart muscle is blocked causing that heart tissue to die from lack oxygen
    "congestiveHeartFailure":1,
    #heart failure heart cant pump enough blood for body's need
    "peripheralVascularDisease":1,
    #narrowed arteries reduce blood flow usually caused by plaque build up atheroscelerosis
    "cerebrovascularDisease":1,
    #leads to strokes brainbleeds cuz affects blood flow to brain
    "dementia":1,
    "chronicPulmonaryDisease":1,
    #lung diseases affecting lungs airway; asthma, bronchitis, emphysema, cystic fibrosis, pulmonary fibrosis
    "rheumaticDisease":1,
    #musculoskeletal and autoimmune conditions: rheumatoid arthrisis, lupus, gou, osteoarthritis
    "pepticUlcerDisease":1,
    #painful sores in stomach lining or upper smal intestine
    "mildLiverDisease":1,
    "diabetesnoChronicComplication":1,
    "diabeteswEndOrganDamage":2,
    "hemiplegia/paraplegia":2,
    #hemi:one side body armleg, para:lowey half both legs waist down
    "renalDisease":2,
    #kidneys damaged cantfitler waste
    "anymalignancy/lymphoma/leukemia":2,
    #blood, bone and lymphatic systme cancers arising from abnormal white blood cell growth
    "moderateoSevereLiverDisease":3,
    "metastaticSolidTumour":6,
    "AIDS/HIV":6,
    "hematologicDisease":1
}

incorconvert = {
    "myocardialInfraction":['Acute myocardial infarction'],
    "congestiveHeartFailure":['Chronic rheumatic heart disease','Valvular disease','Myocarditis and cardiomyopathy','Nonrheumatic and unspecified valve disorders','Cardiac arrest and ventricular fibrillation','Heart failure','Congestive heart failure'],
    "peripheralVascularDisease":['Peripheral and visceral vascular disease','Peripheral vascular disorders','Acute phlebitis; thrombophlebitis and thromboembolism'],
    "cerebrovascularDisease":['Cerebral infarction','Transient cerebral ischemia'],
    "chronicPulmonaryDisease":['Other specified and unspecified upper respiratory disease','Respiratory failure; insufficiency; arrest','Asthma','Pulmonary heart disease','Chronic pulmonary disease','Chronic obstructive pulmonary disease and bronchiectasis','Other specified and unspecified lower respiratory disease','Pneumonia (except that caused by tuberculosis)'],
    "rheumaticDisease":['Systemic lupus erythematosus and connective tissue disorders','Rheumatoid arthritis/collagen vascular diseases','Infective arthritis','Other specified connective tissue disease','Gout','Osteoarthritis','Juvenile arthritis','Autoinflammatory syndromes'],
    "mildLiverDisease":['Liver disease','Biliary tract disease','Hepatitis / Noninfectious hepatitis'],
    "diabetesnoChronicComplication":['Diabetes','Diabetes, uncomplicated','Diabetes mellitus without complication'],
    "diabeteswEndOrganDamage":['Diabetes or abnormal glucose tolerance complicating pregnancy; childbirth; or the puerperium','Diabetes, complicated','Diabetes mellitus with complication'],
    "renalDisease":['Renal disease','Other specified and unspecified diseases of kidney and ureters','Renal failure','Chronic kidney disease','Acute and unspecified renal failure','Urinary incontinence'],
    "anymalignancy/lymphoma/leukemia":['Gastrointestinal cancers - colorectal','Malignant neoplasm, unspecified','Respiratory cancers','Myelodysplastic syndrome (MDS)','Breast cancer - all other types','Multiple myeloma','Gastrointestinal cancers - liver','Gastrointestinal cancers - colorectal','Leukemia - acute myeloid leukemia (AML)','Urinary system cancers - bladder','Male reproductive system cancers - testis','Endocrine system cancers - pancreas','Hodgkin lymphoma','Leukemia - acute lymphoblastic leukemia (ALL)','Gastrointestinal cancers - stomach','Head and neck cancers - lip and oral cavity',
    'Head and neck cancers - laryngeal','Skin cancers - melanoma','Female reproductive system cancers - ovary','Leukemia - chronic myeloid leukemia (CML)','Lymphoma','Non-Hodgkin lymphoma','Head and neck cancers - nasopharyngeal','Head and neck cancers - throat','Head and neck cancers - tonsils','Skin cancers - squamous cell carcinoma','Female reproductive system cancers - cervix','Female reproductive system cancers - endometrium','Female reproductive system cancers - fallopian tube','Female reproductive system cancers - vulva','Female reproductive system cancers - uterus','Endocrine system cancers - adrenocortical','Endocrine system cancers - all other types','Endocrine system cancers - pituitary gland','Endocrine system cancers - thyroid','Male reproductive system cancers - penis'],
    "moderateoSevereLiverDisease":['Hepatic failure'],
    "metastaticSolidTumour":['Metastatic cancer'],
    "AIDS/HIV":['AIDS/HIV'],
    "hematologicDisease": ['Aplastic anemia', 'Coagulation and hemorrhagic disorders', 'Myelodysplastic syndrome (MDS)', 'Hemolytic anemia', 'Deficiency anemia', 'Blood loss anemia']
}

convert = {
    val : charCat
    for charCat, vals in incorconvert.items()
    for val in vals
}


data = data.drop_duplicates(subset=['anon_id','pat_enc_csn_id_coded','order_proc_id_coded','order_time_jittered_utc','comorbidity_component'])

data['charlsonCondition'] = (data['comorbidity_component'].replace(convert))

data['charlsonIndex'] = (data['charlsonCondition'].replace(comorbidityWeights))
data = data[data['charlsonIndex'].notna()]


charlsonConditionsList =['myocardialInfraction','congestiveHeartFailure','peripheralVascularDisease','cerebrovascularDisease','chronicPulmonaryDisease','rheumaticDisease','mildLiverDisease','diabetesnoChronicComplication','diabeteswEndOrganDamage','renalDisease','anymalignancy/lymphoma/leukemia','moderateoSevereLiverDisease','metastaticSolidTumour','AIDS/HIV','hematologicDisease']
data =data[data['charlsonCondition'].isin(charlsonConditionsList)].reset_index(drop=True)


hotCombority = OneHotEncoder(sparse_output = False)

tcomborities = hotCombority.fit_transform(data[['charlsonCondition']])

colCombority = pd.DataFrame(tcomborities, columns = hotCombority.get_feature_names_out())

data = pd.concat([data.drop(columns = ['comorbidity_component_start_days_culture','comorbidity_component_end_days_culture','comorbidity_component']),colCombority],axis=1)


data.to_csv("comorbiditiestesting.csv",index=False)


'''