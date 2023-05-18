# Built using https://towardsdatascience.com/naive-bayes-classifier-how-to-successfully-use-it-in-python-ecf76a995069

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import OrdinalEncoder
from sklearn.naive_bayes import CategoricalNB
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def mfunc(X, y, typ):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    model = typ
    clf = model.fit(X_train, y_train)

    pred_labels = model.predict(X_test)

    print('Classes: ', clf.classes_)
    if str(typ) == 'GaussianNB()':
        print('Class Priors: ', clf.class_prior_)
    else:
        print('Class Log Priors: ', clf.class_log_prior_)

    print('--------------------------------------------------------')
    score = model.score(X_test, y_test)
    print('Accuracy Score: ', score)
    print('--------------------------------------------------------')

    print(classification_report(y_test, pred_labels))
    return X_train, X_test, y_train, y_test, clf, pred_labels

df = pd.read_csv('data.csv')
df.info()

# 'Map' 'Winner' 'Team1StartingSide' 'Team2StartingSide' 'AverageACSTeam1' 'AverageACSTeam2' 'AverageKillsTeam1' 'AverageKillsTeam2' 'TotalFKTeam1' 'TotalFKTeam2' 
# 'TotalFDTeam1' 'TotalFDTeam2' 'TotalKillsTeam1' 'TotalKillsTeam2' 'TotalDeathsTeam1' 'TotalDeathsTeam2' 'TotalFKFDTeam1' 'TotalFKFDTeam2' 'EntryFKFDTeam1' 'EntryFKFDTeam2'
# 'HsPercentageTeam1' 'HsPercentageTeam2'

X = df[['Map', 'Team1StartingSide']]
y = df['Winner'].values

# Encode categorical variables
enc = OrdinalEncoder()
X = enc.fit_transform(X)

frames = [df]
data = pd.concat(frames, axis=1)

#print(df.groupby(['Map', 'Team1StartingSide']).count())

#sns.scatterplot(x="HsPercentageTeam1", y="HsPercentageTeam2", hue='Winner', data=data, palette="tab10")
#sns.displot(x='Team1StartingSide', hue='Winner', col='Map', row='Winner', data=data, rug=True, palette="tab10")
plt.show()

X_train, X_test, y_train, y_test, clf, pred_labels = mfunc(X, y, CategoricalNB())