
$$Pr(Y_{i} = c) = \frac{e_exp{c}}{\sum{i}}$$

# Introducing the MLPM

In the second edition of "An Introduction to Statistical Learning", James, Witten, Hastie, and Tibshirani outline why it is a bad idea to use linear regression for a multi-class classification task. In short, using linear regression 

On the other hand, James et al. also mention that using linear regression for a **binary** classification task is generally not all that problematic, though the authors rightly conclude that such an approach is still undesirable for many reasons, for example because you can get nonsensical predicted probabilities such as -0.2 or 1.5. What James et al. don't mention is that using linear regression on a binary dependent variable is considered a valid approach by mostly economists and sociologists, who refer to such a model as the "linear probability model" or LPM. Some economists and sociologists even go as far as claiming that the LPM is superior to logistic regression, based on poorly-executed simulation studies, but I digress...

That gave me an idea: what if we decompose a multiclass classification problem into a series of LPMs? Would it work? This is essentially the same thing as approximating a multinomial logistic regression model by fitting K-1 binary logistic regressions, where K is the number of classes.

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

My intuition told me that calculating $Pr(y_{i} = 0)$ this way would compound the problem of getting nonsensical predicted probabilities from a "binary LPM". If $Pr(Y_{i} = 1)$ and/or $Pr(Y_{i} = 2)$ can take nonsenical values, $Pr(Y_{i} = 0)$ might get "super nonsensical". For example, if $Pr(Y_{i} = 1) = -0.1$ and $Pr(Y_{i} = 1) = 1.2$, then $Pr(Y_{i} = 0) = 1 - (-0.1) + (1.2) = 2.3$. Obviously, such a result cannot be interpreted in terms of a probability, and I assumed that this fundamental flaw of the "MLPM" would make it a poor classifier. 

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
                           random_state = 1)```


def mlpm(features, target):
  lpm = OneVsRestClassifier(LinearRegression()).fit(features, target)
  y_pred = lpm.predict(features)
  lpm_report = classification_report(target, y_pred, output_dict = True)
  lpm_report = pd.DataFrame(lpm_report).transpose()
  return lpm_report

