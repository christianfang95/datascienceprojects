import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

# Set random seed for reproducibility
np.random.seed(seed=4535)

#Create function to simulate data 
def sim_data(sample_size = 100000, 
             beta_0 = 0.5, 
             beta_1 = 0.2, 
             beta_2 = 1.3, 
             beta_3 = 2,
             beta_4 = 0.8):
             x1 = np.random.random(size = sample_size)
             x2 = np.random.binomial(1, 0.3, size = sample_size)
             x3 = np.random.poisson(lam = 2.5, size = sample_size)
             error = np.random.logistic(loc=0.0, scale=1.0, size = sample_size)
             eta = beta_0 + beta_1 * x1+ beta_2 * x2 + beta_3 * x3 + beta_4 * (x1*x2)
             p = 1 / (1 + np.exp(-eta))
             y1 = np.random.binomial(1, p, size = sample_size)
             y_star = beta_0 + beta_1 * x1 + beta_2 * x2 + beta_3 * x3 + beta_4 * (x1*x2) + error
             d = {'y1' : y1, 'y_star' : y_star, 'x1' : x1, 'x2' : x2, 'x3' : x3}
             return pd.DataFrame(d)

#Simulate data
dat = sim_data()
dat["y2"] = np.select([(dat["y_star"] >= np.mean(dat["y_star"])),
                             (dat["y_star"] < np.mean(dat["y_star"]))], 
                             [1, 0])


#define thresholds
thresholds = np.arange(min(dat['y_star']), 
                       max(dat['y_star']), 
                       0.1)

#Create empty list to store accuracies
accuracy = []

#Calculate accuracy at all thresholds
for i in thresholds:
    y = np.select([(dat['y_star'] >= i),
                   (dat['y_star'] < i)], 
                   [1, 0])
    accuracy.append(accuracy_score(dat['y1'], y))


#Plot accuracy
plt.plot(thresholds, accuracy, linestyle = '-', color = 'black', lw = 2, clip_on = False, label = "correspondence")
plt.vlines(np.mean(dat['y_star']), ymin = 0, ymax = 1, colors="red", label = "mean of y_star")
plt.xlabel('Thresholds to classify y_star as 0 or 1')
plt.ylabel('Correpondence between logistic and linear')
plt.title('Correspondence between logistic transformation \n and linear transformation per threshold')
plt.legend(loc ="lower right")
plt.show()

#Run LPMs and logisitc regressions, get marginal effects form logisitc regressions
lpm1 = smf.ols("y1 ~ x1 + x2 + x3 + (x1*x2)", data=dat).fit()
lpm2 = smf.ols("y2 ~ x1 + x2 + x3 + (x1*x2)", data=dat).fit()
LR1 = smf.logit("y1 ~ x1 + x2 + x3 + (x1*x2)", data=dat).fit()
AME_LR1 = LR1.get_margeff(at='overall', method = 'dydx')
LR2 = smf.logit("y2 ~ x1 + x2 + x3 + (x1*x2)", data=dat).fit()
AME_LR2 = LR2.get_margeff(at='overall', method = 'dydx')

#Populate data frame with coefficients and standard errors
ame_df = pd.DataFrame()
ame_df["X"] = pd.concat([lpm1.params[["x1", "x2", "x3", "x1:x2"]], 
                         lpm2.params[["x1", "x2", "x3", "x1:x2"]], 
                         AME_LR1.summary_frame()["dy/dx"], 
                         AME_LR2.summary_frame()["dy/dx"]])
ame_df["Error"] = pd.concat([lpm1.HC1_se[["x1", "x2", "x3", "x1:x2"]],
                             lpm2.HC1_se[["x1", "x2", "x3", "x1:x2"]],
                             AME_LR1.summary_frame()["Std. Err."],
                             AME_LR2.summary_frame()["Std. Err."]
])
ame_df["Model"] = ["LPM1", "LPM1", "LPM1", "LPM1", 
                   "LPM2", "LPM2", "LPM2", "LPM2", 
                   "LR1", "LR1", "LR1", "LR1", 
                   "LR2", "LR2", "LR2" , "LR2"]
ame_df["Variable"] = ame_df.index

#Logisitcally transformed variable
width = 0.2
x = np.arange(4)
fig, axes = plt.subplots(2, sharex= True)
fig.suptitle('Comparison between LPM coefficients and LR AMEs')
axes[1].bar(x = x, height=ame_df[ame_df["Model"] == "LPM1"]["X"], width=width, yerr=ame_df[ame_df["Model"] == "LPM1"]['Error'], color = "black")
axes[1].bar(x = x + 0.2, height=ame_df[ame_df["Model"] == "LR1"]["X"],  width=width, yerr=ame_df[ame_df["Model"] == "LR1"]['Error'], color = "grey")
axes[1].set_xticks(x+0.1, ["x1", "x2", "x3", "x1*x2"])
axes[1].title.set_text('Logistically transformed DV')
axes[0].bar(x = x, height=ame_df[ame_df["Model"] == "LPM2"]["X"], width=width, yerr=ame_df[ame_df["Model"] == "LPM2"]['Error'], color = "black")
axes[0].bar(x = x + 0.2, height=ame_df[ame_df["Model"] == "LR2"]["X"],  width=width, yerr=ame_df[ame_df["Model"] == "LR2"]['Error'], color = "grey")
axes[1].set_ylabel("Estimates")
axes[0].set_ylabel("Estimates")
axes[0].title.set_text('Linearly transformed DV')
axes[0].legend(["LPM", "LR"])
fig.tight_layout()
plt.show()







