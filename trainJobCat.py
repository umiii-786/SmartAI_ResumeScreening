from customTransformers.preproccessingTransformer import CleanData
from customTransformers.stemmingTransformer import ApplyStemming
from customTransformers.StopWordTransformer import RemoveStopWords
from sklearn.preprocessing import LabelEncoder
import pandas as pd 
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import nltk 
import pickle

data=pd.read_csv('./Data/job_title_des.csv')
lbl=LabelEncoder()
y=lbl.fit_transform(data['Job Title'])
x=data.drop(columns=['Job Title','Unnamed: 0'],axis=1)

xgparams2={'booster': 'gbtree',
    'n_estimators': 100,
    'learning_rate': 0.05,
    'max_depth': 1,
    'min_child_weight': 3,
    'gamma': 0.2,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'colsample_bylevel': 0.9,
    'colsample_bynode': 0.9,
    'reg_alpha': 0.5,
    'reg_lambda': 1.0,
    'tree_method': 'auto',
    'objective': 'multi:softprob',
    'eval_metric': 'logloss',
    'nthread': 4}

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=34)
print(x_train.shape)
print(x_test.shape)
pipe=Pipeline(steps=[
    ("preprocessing data",CleanData()),
    ("removing stopwords",RemoveStopWords()),
    ("applied stemming",ApplyStemming()),
    ("Applying Vectorizing",TfidfVectorizer(max_features=1000)),
    ('Model Applied',XGBClassifier(**xgparams2))
])

pipe.fit(x_train,y_train)

with open('./model.pkl','wb') as mf:
    pickle.dump(pipe,mf)it 
with open('./label.pkl','wb') as lb:
    pickle.dump(lbl,lb)
# y_pred=pipe.predict(x_test)
# print(accuracy_score(y_test,y_pred=y_pred))
# trainY=pipe.predict(x_train)
# print(accuracy_score(y_train,y_pred=trainY))
# print(data)

