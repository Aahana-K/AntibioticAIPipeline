This is a 2 stage machine learning pipeline identifying potential bacterial infections and recommending likely effective treatment

#mainy.py - preprocessing(some parts deleted as new steps were needed but some were already implemented)

antibioticAI.py - randomForest model for second stage of pipeline

app.py - flask app connecting the two models to user interface and running LIME(explaining choice for second stage)

stage1antibioticAI.py - ensemble model for first stage of pipeline

form.html - page for entering in patient info to AI

index.html - home page

urinrCultures.py - one of testing files, included to show a different approach I tried for the pipeline
