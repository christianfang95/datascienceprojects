#import required packages
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt
import random
#Set seed
np.random.seed(4375)

#Define function to simulate logisitc regression data
def sim_logistic_data(sample_size = 1000, 
                      beta_0 = -0.20, 
                      beta_1 = -0.5, 
                      beta_2 = 1.5, 
                      beta_3 = 1):
    x1 = np.random.random(size = sample_size)
    x2 = np.random.binomial(1, 0.3, size = sample_size)
    x3 = np.random.poisson(lam = 2.5, size = sample_size)
    eta = beta_0 + beta_1 * x1+ beta_2 * x2 + beta_3 * x3
    p = 1 / (1 + np.exp(-eta))
    y = np.random.binomial(1, p, size = sample_size)
    y = np.random.binomial(1, p, sample_size)
    d = {'y' : y, 'x1' : x1, 'x2' : x2, 'x3' : x3}
    return pd.DataFrame(d)

#Get data
example_data = sim_logistic_data()
example_data.head()

#Fitting logistic regression and getting predicted labels
#Splitting the X and Y

regression =  smf.logit("y ~ x1 + x2 + x3", data = example_data).fit()

#Predict labels
predicted_labels_logit = regression.predict()

#Get actual labels
actual_labels = example_data['y']

#Define thresholds
thresholds = np.arange(0, 1, 0.001)

#Extract number of positive and negative examples in the data
P = len(example_data[example_data['y'] == 1])
N = len(example_data[example_data['y'] == 0])

#Initialize FPR and TPR
FPR_logit = []
TPR_logit = []

#
for i in thresholds:
    FP=0
    TP=0
    thresh = round(i,2) #Limiting floats to two decimal points, or threshold 0.6 will be 0.6000000000000001 which gives FP=0
    for j in range(len(predicted_labels_logit)):
        if (predicted_labels_logit[j] >= thresh):
            if actual_labels[j] == 1:
                TP = TP + 1
            if actual_labels[j] == 0:
                FP = FP + 1
    FPR_logit.append(FP/N)
    TPR_logit.append(TP/P)

#
#roc_data = {"TPR": TPR_logit, "FPR": FPR_logit}
#roc_df_logit = pd.DataFrame(roc_data).sort_values(by = ["TPR", "FPR"])
#roc_df_logit["dFPR"] = np.diff(roc_df_logit["FPR"], 0)
#roc_df_logit["dTPR"] = np.diff(roc_df_logit["TPR"], 0)
#sum(TPR * dFPR) + sum(dTPR * dFPR)/2

#def auc(TPR, FPR):
#    dFPR = np.diff(FPR, 0)
#    dTPR = np.diff(TPR, 0)
#    auc = (sum(TPR * dFPR) + sum(dTPR * dFPR)) / 2
#    return auc

#aauc = auc(TPR_logit, FPR_logit)

roc_data = {"TPR": TPR_logit, "FPR": FPR_logit}
roc_df_logit = pd.DataFrame(roc_data).sort_values(by = ["TPR", "FPR"])

#Calculate AUC

auc = np.trapz(roc_df_logit["TPR"], roc_df_logit["FPR"])

#Plot figure
plt.plot(roc_df_logit["FPR"], roc_df_logit["TPR"], linestyle='-', color='black', lw = 2, label='ROC ', clip_on=False)
plt.plot([0, 1], [0, 1], color='grey', linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('FPR (1-Specificity)')
plt.ylabel('TPR (Sensitivity)')
plt.title('ROC curve of Logistic Regression, AUC = %.2f'%auc)
plt.legend(loc="lower right")
plt.show()
