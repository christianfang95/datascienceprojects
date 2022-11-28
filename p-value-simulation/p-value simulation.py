import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import seaborn as sns

#Simulate linear regression data
def sim_data(sample_size = 1000, beta_0 = 1, beta_1 = 0.00):
  """ This function simulates a simple linear regression consisting of two 
  predicors: the intercept and x1
  """
  x1 = np.random.random(size = sample_size)
  error = np.random.random(size = sample_size)
  y = beta_0 + beta_1 * x1 + error
  d = {'y' : y, 'x1' : x1}
  return pd.DataFrame(d)

#Perform simulation
def getpvalue(repetitions = 2000, sample_size = 100):
  """ This function runs 1000 linear regressions with different values
  for the slope of x1, and appends the results to a list
  """
  b = [0.00, 0.001, 0.01, 0.05, 0.10]
  res = []
  for i in range(repetitions):
      data = sim_data(sample_size = sample_size, beta_1 = b[0])
      regression = smf.ols("y ~ x1", data = data).fit()
      pval_x1 = regression.pvalues["x1"]
      res.append([b[0], pval_x1, sample_size])
      data = sim_data(sample_size = sample_size, beta_1 = b[1])
      regression = smf.ols("y ~ x1", data = data).fit()
      pval_x1 = regression.pvalues["x1"]
      res.append([b[1], pval_x1, sample_size])
      data = sim_data(sample_size = sample_size, beta_1 = b[2])
      regression = smf.ols("y ~ x1", data = data).fit()
      pval_x1 = regression.pvalues["x1"]
      res.append([b[2], pval_x1, sample_size])
      data = sim_data(sample_size = sample_size, beta_1 = b[3])
      regression = smf.ols("y ~ x1", data = data).fit()
      pval_x1 = regression.pvalues["x1"]
      res.append([b[3], pval_x1, sample_size])
      data = sim_data(sample_size = sample_size, beta_1 = b[4])
      regression = smf.ols("y ~ x1", data = data).fit()
      pval_x1 = regression.pvalues["x1"]
      res.append([b[4], pval_x1, sample_size])
  return res

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

size = [2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
2000, 3000, 4000, 5000, 6000, 7000, 8000, 10000, 20000, 40000, 60000, 80000, 100000]


def main():
  result = []
  count = 0
  for sample in size:
    count += 1
    result.append(getpvalue(sample_size = sample))
    print("Ran sample " +str(count) + " out of " + str(len(size)) + ". " +
     str((100*(count/len(size)))) + " % done.")
  flat_list = flatten_list(result)
  df = pd.DataFrame(flat_list).rename(columns = {0: "ES b", 1: "p-value x1", 2: 'sample size'})
  return df



df = main()

#Plot p-values
fig, axes = plt.subplots(2, 3, figsize = (15, 7.5))
fig.suptitle('Distribution of p-values of Linear Regression Coefficients of Different Magnitudes, N=1000', 
             fontsize = 18, 
             y = 1.05)
fig.subplots_adjust(top = 0.5)
sns.color_palette("rocket")
fig.tight_layout(pad=1.0)
axes[0, 0].set_title('$b_1$ = 0.00', fontsize = 15, pad = 5)
axes[0, 1].set_title('$b_1$ = 0.01', fontsize = 15, pad = 5)
axes[0, 2].set_title('$b_1$ = 0.02', fontsize = 15, pad = 5)
axes[1, 0].set_title('$b_1$ = 0.03', fontsize = 15, pad = 5)
axes[1, 1].set_title('$b_1$ = 0.04', fontsize = 15, pad = 5)

#sns.histplot(ax = axes[0, 0], data = df, x = df[df["ES b"] == 0.0]['p-value x1'], hue='sample size', bins = 50, palette = colors)
sns.lineplot(ax = axes[0, 0], data = df, x=df['sample size'], y = df[df["ES b"] == 0.0]['p-value x1'], ci=None)
sns.lineplot(ax = axes[0, 1], data = df, x=df['sample size'], y = df[df["ES b"] == 0.001]['p-value x1'])
sns.lineplot(ax = axes[0, 2], data = df, x=df['sample size'], y = df[df["ES b"] == 0.01]['p-value x1'])
sns.lineplot(ax = axes[1, 0], data = df, x=df[df['sample size'] < 20000]['sample size'], y = df[df["ES b"] == 0.05]['p-value x1'])
sns.lineplot(ax = axes[1, 1], data = df, x=df[df['sample size'] < 20000]['sample size'], y = df[df["ES b"] == 0.1]['p-value x1'])
axes[0, 0].set_ylim(0,1)
axes[0, 1].set_ylim(0,1)
axes[0, 2].set_ylim(0,1)
axes[1, 0].set_ylim(0,1)
axes[1, 1].set_ylim(0,1)
axes[1, 2].set_visible(False)
axes[1, 0].set_position([0.24,0.125,0.228,0.343])
axes[1, 1].set_position([0.55,0.125,0.228,0.343])
fig.show()
