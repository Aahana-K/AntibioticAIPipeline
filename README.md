This is a 2 stage machine learning pipeline identifying potential bacterial infections and recommending likely effective treatment

mainy.py - preprocessing(some parts deleted as new steps were needed but some were already implemented)

antibioticAI.py - code for second stage of pipeline

main.py - flask app connecting the two models to user interface and running LIME(explaining choice for second stage)

