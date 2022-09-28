import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score

#Set random seed for reproducibility
np.random.seed(seed=4535)

def sim_data(sample_size = 100000, 
             beta_0 = 0.5, 
             beta_1 = 0.5, 
             beta_2 = 0.5, 
             beta_3 = 0.5):
             x1 = np.random.random(size = sample_size)
             x2 = np.random.binomial(1, 0.3, size = sample_size)
             x3 = np.random.poisson(lam = 2.5, size = sample_size)
             error = np.random.logistic(loc=0.0, scale=1.0, size = sample_size)
             eta = beta_0 + beta_1 * x1+ beta_2 * x2 + beta_3 * x3
             p = 1 / (1 + np.exp(-eta))
             y1 = np.random.binomial(1, p, size = sample_size)
             y_star = beta_0 + beta_1 * x1+ beta_2 * x2 + beta_3 * x3 + error
             y2 = np.select([(y_star >= np.mean(y_star)),
                             (y_star < np.mean(y_star))], 
                             [1, 0])
             d = {'y1' : y1, 'y2' : y2, 'y_star' : y_star, 'x1' : x1, 'x2' : x2, 'x3' : x3}
             return pd.DataFrame(d)

#Simulate data
dat = sim_data()


#Confusion matrix
cm = confusion_matrix(y_true = dat['y1'], y_pred = dat['y2'])
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()

#Calculate accuracy
accuracy = accuracy_score(dat['y1'], dat['y2'])
accuracy 

#Correlation between variable

statistics.corrrelation(dat['y1'],dat['y2'])


#Plot y vs. y_star
#sns.scatterplot(data = dat, x = "y_star", y = "y2")

#Plot y1 vs y2
#sns.scatterplot(data = dat, x = "y2", y = "y1")

