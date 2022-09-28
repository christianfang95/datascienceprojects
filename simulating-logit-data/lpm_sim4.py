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
             y_star = beta_0 + beta_1 * x1 + beta_2 * x2 + beta_3 * x3 + error
             y2 = np.select([(y_star >= np.mean(y_star)),
                             (y_star < np.mean(y_star))], 
                             [1, 0])
             d = {'y1' : y1, 'y2' : y2, 'x1' : x1, 'x2' : x2, 'x3' : x3}
             return pd.DataFrame(d)

#Create lists for variables
beta0 = list(np.around(np.linspace(0, 1), 2))
beta1 = list(np.around(np.linspace(1, 2), 2))
beta2 = list(np.around(np.linspace(-1, 0), 2))
beta3 = list(np.around(np.linspace(-0.5, 0.5), 2))
result_x = []

for x in range(len(beta0)-1):
    dat = sim_data(beta_0=beta0[x], beta_1=beta1[x], beta_2=beta2[x], beta_3=beta3[x])
    lpm1 = smf.ols("y1 ~ x1 + x2 + x3", data=dat).fit()
    lpm2 = smf.ols("y2 ~ x1 + x2 + x3", data=dat).fit()
    LR1 = smf.logit("y1 ~ x1 + x2 + x3", data=dat).fit().get_margeff(at='overall', method = 'dydx')
    LR2 = smf.logit("y2 ~ x1 + x2 + x3", data=dat).fit().get_margeff(at='overall', method = 'dydx')
    result_x.append([pd.concat([lpm1.params[["x1", "x2", "x3"]], lpm2.params[["x1", "x2", "x3"]], LR1.summary_frame()["dy/dx"], LR2.summary_frame()["dy/dx"]])])

arr = np.array(result_x).T.reshape(12, 49)
df = pd.DataFrame(arr)
df["X"] = ["X1", "X2", "X3", "X1", "X2", "X3", "X1", "X2", "X3", "X1", "X2", "X3"]
df["Model"] = ["LPM1", "LPM1", "LPM1", "LPM2", "LPM2", "LPM2", "LR1", "LR1", "LR1", "LR2", "LR2", "LR2"]

#We want to visualize the average differences between the LPM and LR coefficients for every x1, x2, x3

copy = pd.DataFrame(arr)
copy = copy.diff(periods=6)
copy = copy.drop([0,1, 2, 3, 4, 5])
copy["Label"] = ["X1 nonlin", "X2 nonlin", "X3 nonlin", "X1 lin", "X2 lin", "X3 lin"]

#Visualize average differences

#Plot for X1

plt.scatter(x=df[(df["X"] == "X1") & (df["Model"] == "LPM1")].iloc[:, 0:48], 
            y = df[(df["X"] == "X1") & (df["Model"] == "LR1")].iloc[:, 0:48])
plt.scatter(x=df[(df["X"] == "X1") & (df["Model"] == "LPM2")].iloc[:, 0:48], 
            y = df[(df["X"] == "X1") & (df["Model"] == "LR2")].iloc[:, 0:48])
plt.scatter(x=df[(df["X"] == "X2") & (df["Model"] == "LPM1")].iloc[:, 0:48], 
            y = df[(df["X"] == "X2") & (df["Model"] == "LR1")].iloc[:, 0:48])
plt.scatter(x=df[(df["X"] == "X2") & (df["Model"] == "LPM2")].iloc[:, 0:48], 
            y = df[(df["X"] == "X2") & (df["Model"] == "LR2")].iloc[:, 0:48])
plt.scatter(x=df[(df["X"] == "X3") & (df["Model"] == "LPM1")].iloc[:, 0:48], 
            y = df[(df["X"] == "X3") & (df["Model"] == "LR1")].iloc[:, 0:48])
plt.scatter(x=df[(df["X"] == "X3") & (df["Model"] == "LPM2")].iloc[:, 0:48], 
            y = df[(df["X"] == "X3") & (df["Model"] == "LR2")].iloc[:, 0:48])










copy[(copy["X"] == "X1") & (copy["Model"] == "LPM1")] - copy[(copy["X"] == "X1") & (copy["Model"] == "LR1")]






pt = pd.pivot_table(copy, index = ["X"], columns = ["Model"])
pt
pt["Diff_nonlinear"] = pt["LR1"] - pt["LPM1"]


c = copy.groupby(["Model", "X"]).diff()







#Run LPMs and logisitc regressions, get marginal effects form logisitc regressions
lpm1 = smf.ols("y1 ~ x1 + x2 + x3", data=dat).fit()
lpm2 = smf.ols("y2 ~ x1 + x2 + x3", data=dat).fit()
LR1 = smf.logit("y1 ~ x1 + x2 + x3", data=dat).fit()
AME_LR1 = LR1.get_margeff(at='overall', method = 'dydx')
LR2 = smf.logit("y2 ~ x1 + x2 + x3", data=dat).fit()
AME_LR2 = LR2.get_margeff(at='overall', method = 'dydx')

#Populate data frame with coefficients and standard errors
ame_df = pd.DataFrame()
ame_df["X"] = pd.concat([lpm1.params[["x1", "x2", "x3"]], lpm2.params[["x1", "x2", "x3"]], AME_LR1.summary_frame()["dy/dx"], AME_LR2.summary_frame()["dy/dx"]])
ame_df["Error"] = pd.concat([lpm1.HC1_se[["x1", "x2", "x3"]],
                             lpm2.HC1_se[["x1", "x2", "x3"]],
                             AME_LR1.summary_frame()["Std. Err."],
                             AME_LR2.summary_frame()["Std. Err."]
])
ame_df["Model"] = ["LPM1", "LPM1", "LPM1", "LPM2", "LPM2", "LPM2", "LR1", "LR1", "LR1", "LR2", "LR2", "LR2" ]
ame_df["Variable"] = ame_df.index

#Logisitcally transformed variable
width = 0.2
x = np.arange(3)
fig, axes = plt.subplots(2, sharex= True)
fig.suptitle('Comparison between LPM coefficients and LR AMEs')
axes[0].bar(x = x, height=ame_df[ame_df["Model"] == "LPM1"]["X"], width=width, yerr=ame_df[ame_df["Model"] == "LPM1"]['Error'], color = "black")
axes[0].bar(x = x + 0.2, height=ame_df[ame_df["Model"] == "LR1"]["X"],  width=width, yerr=ame_df[ame_df["Model"] == "LR1"]['Error'], color = "grey")
axes[0].set_xticks(x+0.1, ["x1", "x2", "x3"])
axes[0].title.set_text('Logistically transformed DV')
axes[1].bar(x = x, height=ame_df[ame_df["Model"] == "LPM2"]["X"], width=width, yerr=ame_df[ame_df["Model"] == "LPM2"]['Error'], color = "black")
axes[1].bar(x = x + 0.2, height=ame_df[ame_df["Model"] == "LR2"]["X"],  width=width, yerr=ame_df[ame_df["Model"] == "LR2"]['Error'], color = "grey")
axes[0].set_ylabel("Estimates")
axes[1].set_ylabel("Estimates")
axes[1].title.set_text('Linearly transformed DV')
axes[0].legend(["LPM", "LR"])
fig.tight_layout()
plt.show()







