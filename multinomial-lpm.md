# Introducing the MLPM

In the second edition of "An Introduction to Statistical Learning", James, Witten, Hastie, and Tibshirani outline why it is a bad idea to use linear regression for a multi-class classification task. In short, the regression coefficients and predicted probabilities are dependent on the ordering of the classes (e.g., ordering the classes as [0, 1, 2] will give you different results compared to ordering the classes as [1, 0, 2]), and linear regression assumes that the difference between the classes is equally big (which makes no sense when you talk about an ordinal variable). 

On the other hand, James et al. also mention that using linear regression for a **binary** classification task is generally not all that problematic, though the authors rightly conclude that such an approach is still undesirable for many reasons, for example because you can get nonsensical predicted probabilities such as -0.2 or 1.5. What James et al. don't mention is that using linear regression on a binary dependent variable is considered a valid approach by mostly economists and sociologists, who refer to such a model as the "linear probability model" or LPM. Some economists and sociologists even go as far as claiming that the LPM is superior to logistic regression, based on poorly-executed simulation studies, but I digress...

That gave me an idea: what if we decompose a multiclass classification problem into a series of LPMs? Would it work, as in: would the prediction performance be at least reasonably high to warrant the use of such a model? After all, estimating a series of LPMs is basically the same thing as approximating a multinomial logistic regression model by fitting K-1 binary logistic regressions, where K is the number of classes. 

Note: Please take this tutorial with a grain of salt. As you will see from my conclusion, I do not recommend using the MLPM as a classification algorithm. 

## Mathematical notation for the MLPM

The joke about the MLPM is that is is merely a series of separate linear



I am not 100% sure about the mathematical notation for the "multinomial LPM" (since I just made it up...), but it should be something like this:

$$Pr(Y_{i} = k) = \alpha + \sum_{j=1}^{k-1} \beta_{k}X_{i}$$

In other words, we fit K-1 linear probability models 

## An example using three classes

If we have three classes, [0, 1, 2], then we would simply fit two LPMs:

$$Pr(Y_{i} = 1) = \alpha + \sum \beta_{i}X_{i}$$

$$Pr(Y_{i} = 2) = \alpha + \sum \beta_{i}X_{i}$$

This gives us the predicted probabilities of each row being 1 or 2, respectively. But what about the proability of being 0? Well, the only way I came up with was to simply define $Pr(y_{i} = 0)$ as follows:

$$Pr(Y_{i} = 0) = 1 - Pr(Y_{i} = 1) - Pr(Y_{i} = 2) $$

My intuition told me that calculating $Pr(y_{i} = 0)$ this way would compound the problem of getting nonsensical predicted probabilities from a "binary LPM". If $Pr(Y_{i} = 1)$ and/or $Pr(Y_{i} = 2)$ can take nonsenical values, $Pr(Y_{i} = 0)$ might get "super nonsensical". For example, if $Pr(Y_{i} = 1) = -0.1$ and $Pr(Y_{i} = 1) = 1.2$, then $Pr(Y_{i} = 0) = 1 - (0.3) - (1.4) = -0.7$. Obviously, such a result cannot be interpreted in terms of a probability, and I assumed that this fundamental flaw of the "MLPM" would make it a poor classifier. 

Little did I know...

# Does it work?

There are multiple ways of estimating an "MLPM". In principle, we would just need to make dummy variables out of the target variable, fit K-1 LPMs, calculate the K-1 predicted probabilities, and calculate $Pr(y_{i} = 0)$ as stated above. 

An easier way is to use the `OneVsRestClassifier` from `sklearn.multiclass`, which breaks down a multiclass classification problem into a series of binary classification tasks. 

## Importing packages and simulating data

First, let's import the required packages and simulate some data for a 5-class classification problem using `make_classification` from `sklearn.datasets`:

```python
#Import required packages
import pandas as pd
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
```

```python
# simulate dataset
classes = 4
X, y = make_classification(n_samples = 1000, 
                           n_features = 10, 
                           n_informative = 3, 
                           n_redundant = 7, 
                           n_classes = classes, 
                           random_state = 1)
 ```
 
 ## Implementing the MLPM
 
 Next, we implement our state-of-the-art multinomial linear probability model by passing `LinearRegression()` from `sklearn.linear_model` to the `OneVsRestClassifier`. We, then, calculate the predicted proabilities and get the `classification_report` as a Pandas data frame.

```python
def mlpm(features, target):
  lpm = OneVsRestClassifier(LinearRegression()).fit(features, target)
  y_pred = lpm.predict(features)
  lpm_report = classification_report(target, y_pred, output_dict = True)
  lpm_report = pd.DataFrame(lpm_report).transpose()
  return lpm_report
 ```
## Implementing relevant baselines: multinomial logistic regression and K nearest neighbors

To gauge the performance of the MLPM (esp. in terms of the F1 score for each class), I implemented two "outdated" alternatives to the MLPM ("outdated" as the MLPM is super novel, from 2022!), namely multinomial logistic regression and K nearest neighbors. Multinomial logistic regression is an extension of logistic regression (a parametric supervised learning algorithm), and K nearest neighbors (a non-parametric supervised learning method).

I defined two functions for multinomial logistic regression and KNN, respecitively:

```python
def multinom(features, target):
  multinom = OneVsRestClassifier(LogisticRegression(multi_class = "multinomial")
                                ).fit(features, target)
  y_pred = multinom.predict(features)
  multinom_report = classification_report(target, y_pred, output_dict = True)
  multinom_report = pd.DataFrame(multinom_report).transpose()
  return multinom_report
  
def knn(features, target):
  knn = KNeighborsClassifier(n_neighbors = classes).fit(features, target)
  y_pred = knn.predict(features)
  knn_report = classification_report(target, y_pred, output_dict = True)
  knn_report = pd.DataFrame(knn_report).transpose()
  return knn_report
 ```
 
 ## Plotting the results
 
 Lastly, I define a function to plot the results and wrap all previous functions in a main function:
 
 ```python
 def plot(lpm, log, knn):
  #Set style
  sns.set_style('darkgrid')

  #Initialize plot, set title
  fig, ax = plt.subplots(nrows = 1, sharex = True)
  fig.suptitle('F1 scores of multinomial regressions and KNN', y = 1.04)
  
  #Add lines for the 3 models
  sns.lineplot(x = lpm.index[:-3], y = lpm['f1-score'][-3], marker = 'o')
  sns.lineplot(x = log.index[:-3], y = log['f1-score'][-3], marker = 'o')
  sns.lineplot(x = knn.index[:-3], y = knn['f1-score'][-3], marker = 'o')
  
  #Set axes title, label, and legend
  ax.set_title('F1 score')
  ax.set_ylabel('F1 score')
  ax.legend(('linear regression', 'logistic regression', 'KNN'))

  #Plot formatting
  plt.subplots_adjust(hspace = 0.4)
  plt.ylim([0, 1])
  plt.xticks(rotation = 90)
  plt.show()

def main(features, target):
    mod1 = mlpm(features, target)
    mod2 = multinom(features, target)
    mod3 = knn(features, target)
    plot2(mod1, mod2, mod3)
    plt.show()
 ```
 
 # The result: how well does the MLPM perform?
 
 Now, all there is left to do is to call our main function and examine the resulting plot showing the F1 scores of the three models:
 
 ```python
 
 main(X, y)
 ```
 
 The plot shows us that - perhaps shockingly enough - the MLPM does not perform all that terribly.
 
  
 
 

