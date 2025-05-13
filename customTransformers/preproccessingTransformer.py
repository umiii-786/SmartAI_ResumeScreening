import re
from sklearn.base import BaseEstimator, TransformerMixin
import pandas 
import string

class CleanData(BaseEstimator,TransformerMixin):
  def __init__(self):
    pass
  def fit(self,x,y=None):
    return self
  def transform(self,x):
    x=x.copy()
    x.iloc[:,0]=x.iloc[:,0].apply(self.removeUglyMaterial)
    return x

  def removeUglyMaterial(self,x):
      punctuations=string.punctuation
      punctuations+="₹\n"
      pattern = f"[{re.escape(punctuations)}]"
      preprocessed=re.sub(pattern, " ", x)
      preprocessed=re.sub(r"\d+", "", preprocessed)
      # print(preprocessed)
      preprocessed=re.sub(r"\s+", " ", preprocessed)
      preprocessed=preprocessed.strip()
      preprocessed=preprocessed.lower()

      return preprocessed
  

