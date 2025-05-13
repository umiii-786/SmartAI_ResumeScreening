
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.stem.porter import PorterStemmer
class ApplyStemming(BaseEstimator,TransformerMixin):
  def __init__(self):
    pass
  def fit(self,x,y=None):
    return self
  def transform(self,x):
    x=x.copy()
    x.iloc[:,0]=x.iloc[:,0].apply(self.ApplySteming)
    # text=" ".join(x.iloc[:,0])
    return x.iloc[:,0]

  def ApplySteming(self,x):
    stemWords=[]
    for word in x.split(' '):
      stem=PorterStemmer()
      stemWord=stem.stem(word)
      stemWords.append(stemWord)
    return " ".join(stemWords)