import pandas as pd
from customTransformers.preproccessingTransformer import CleanData
from customTransformers.stemmingTransformer import ApplyStemming
from customTransformers.StopWordTransformer import  RemoveStopWords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer

overall_Desc=pd.read_csv('./Data/jobOverallDescription.csv')


def PerfectionScore(jobtitle,userDescription):
        
    pipe=Pipeline(steps=[
        ('preproceed Data',CleanData()),
        ('RemoveStopWords',RemoveStopWords()),
        ('Applying Stemming',ApplyStemming()),
        ('Vectorizing',CountVectorizer())
    ])

    targetDescription=overall_Desc[overall_Desc['Job Title']==jobtitle]['Overall Description']
    pipe.fit(pd.DataFrame(targetDescription))
    overDescVector=pipe.transform(pd.DataFrame(targetDescription))
    userDescVector=pipe.transform(pd.DataFrame(userDescription))

    score=cosine_similarity(overDescVector,userDescVector)
    return score[0][0]


