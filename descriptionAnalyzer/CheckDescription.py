from customTransformers.preproccessingTransformer import CleanData
from customTransformers.StopWordTransformer import RemoveStopWords
from customTransformers.stemmingTransformer import ApplyStemming
import os 
import cloudpickle
import pandas as pd 
from sklearn.preprocessing import LabelEncoder

def ProcessDescription(description):
    # print(description)
    currentDir=os.path.dirname(__file__)
    Modelfullpath=os.path.join(currentDir,'model.pkl')
    Labelfullpath=os.path.join(currentDir,'label.pkl')
    file=open('model.pkl','rb')
    labelFile=open('label.pkl','rb')
    pipe=cloudpickle.load(file=file)
    labels=cloudpickle.load(file=labelFile)
    predictCategory=pipe.predict(pd.DataFrame(description))
    category=labels.inverse_transform(predictCategory)
    return category[0]