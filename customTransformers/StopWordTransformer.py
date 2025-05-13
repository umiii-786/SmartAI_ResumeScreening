# from nltk.tokenizer import W
from sklearn.base import BaseEstimator, TransformerMixin
import pandas
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class RemoveStopWords(BaseEstimator,TransformerMixin):
  def __init__(self):
    pass
  def fit(self,x,y=None):
    return self
  def transform(self,x):
    x=x.copy()
    x.iloc[:,0]=x.iloc[:,0].apply(self.removeStopWords)
    return x

  def removeStopWords(self,x):
      stop_words = set(stopwords.words('english'))
      notStopWords=[]
      for word in word_tokenize(x):
        if word not in  stop_words:
          notStopWords.append(word)
      return " ".join(notStopWords)