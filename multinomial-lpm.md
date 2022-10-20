# Introducing the MLPM

In the second edition of "An Introduction to Statistical Learning", James, Witten, Hastie, and Tibshirani outline [why it is a bad idea to use linear regression for a multi-class classification task](https://hastie.su.domains/ISLR2/ISLRv2_website.pdf). In short, the regression coefficients and predicted probabilities are dependent on the ordering of the classes (e.g., ordering the classes as [0, 1, 2] will give you different results compared to ordering the classes as [1, 0, 2]), and linear regression assumes that the difference between the classes is equally big (which makes no sense when you talk about a qualitative target variable). 

On the other hand, James et al. also mention that using linear regression for a *binary* classification task is generally not all that problematic, though the authors rightly conclude that such an approach is still undesirable for many reasons, for example because you can get nonsensical predicted probabilities such as -0.2 or 1.5. What James et al. don't mention is that using linear regression on a binary dependent variable *is* considered a valid approach by mostly economists and sociologists, who refer to such a model as a "linear probability model" or LPM. Some economists and sociologists even go as far as claiming that the LPM is superior to logistic regression, based on poorly-executed simulation studies, but I digress...

That gave me an idea: what if we decompose a multiclass classification problem into a series of LPMs? Would it work, as in: would the prediction performance be at least reasonably high to warrant the use of such a model? After all, estimating a series of LPMs is sort of the same thing as approximating a multinomial logistic regression model by fitting n-1 binary logistic regressions, where n is the number of classes. 

Note: *Please take this tutorial with a grain of salt. The LPM and MLPM are stupid. As you will see from my conclusion, I do not recommend using the MLPM as a classification algorithm.*

## Inventing the MLPM

The "multinomial linear probability model" is not actually a proper statistical model, it is just a series separate "binary" linear probability models. I am not 100% sure about how you would mathematically describe the MLPM (since I just made it up...), but it should be something like this:

$$Pr(Y_{i} = k) = \alpha + \sum_{j=1}^{k-1} \beta_{k}X_{i}$$

In other words, if we have $k$ classes to predict, we fit $k$ separate binary LPMs. For example, if we have three classes, [0, 1, 2], then we would simply fit three LPMs:

$$Pr(Y_{i} = 0) = \alpha + \sum \beta_{i}X_{i}$$

$$Pr(Y_{i} = 1) = \alpha + \sum \beta_{i}X_{i}$$

$$Pr(Y_{i} = 2) = \alpha + \sum \beta_{i}X_{i}$$

This gives us three predicted probabilities: 
- the probability of the observation being in class 0 (as opposed to 1 and 2)
- the probability of the observation being in class 1 (as opposed to 0 and 2)
- the probability of the observation being in class 2 (as opposed to 0 and 1)


My intuition told me that this is a deeply weird approach. As described above, the problem with the LPM is that it can yield predicted probabilities outside the unit interval [0,1]. This is not the case when using a model that explicitly places constraints on the range of the predicted probabilities, such as (multinomial) logistic regression. In case of, for example, multinomial logistic regression, the sum of the predicted probabilities will always be exactly 1. In case of the MLPM, there are no constraints on the range of the predicted probabilities, which may imply that 

$$Pr(Y_{i} = 0) + Pr(Y_{i} = 1) + Pr(Y_{i} = 2) > 1$$

or even 

$$Pr(Y_{i} = 0) + Pr(Y_{i} = 1) + Pr(Y_{i} = 2) < 1$$


Obviously, this makes absolutely no sense, and I assumed that this fundamental flaw of the "MLPM" would make it a poor classifier. 

Little did I know...

# (How) does it work?

There are multiple ways of estimating an "MLPM". In principle, we could just make dummy variables out of the target variable, fit K LPMs and calculate the K predicted probabilities.

An easier way is to use the `OneVsRestClassifier` from `sklearn.multiclass`, which breaks down a multiclass classification problem into a series of binary classification tasks. Usually, you would use it with a logistic regression, but we can simply use a linear regression model instead! ;)

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

To gauge the performance of the MLPM (esp. in terms of the F1 score for each class), I implemented two "outdated" alternatives to the MLPM ("outdated" as the MLPM is super novel, from 2022!!), namely multinomial logistic regression and K nearest neighbors. Multinomial logistic regression is an extension of logistic regression (a parametric supervised learning algorithm), and K nearest neighbors (a non-parametric supervised learning method).

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
 
 ![](/images/mlpm.png)

 
 
 The plot shows us that - perhaps shockingly enough - the MLPM does not perform all that terribly. It is only slightly worse than multinomial logistic regression, though when compared to KNN, both the MLPM and multinomial logistic regression don't perform that well.
 
 # Conclusion
 
Well, I guess the MLPM sort of works for classification tasks. This is perhaps unsurprising, as multinomial logistic regression basically just estimates linear models and applies a transformation to keep the predicted probabilities bound to the unit interval [0,1]. 
 
Does this mean you should use the MLPM? Probably not. I am not really a fan of the "anything goes" type of data science (which is a stereotype about data scientists some/many academics hold btw), the MLPM still does not make substantive sense, as out-of-range predicted probabilities are just not useful. 

For classification tasks, a vanilla multinomial logistic regression performs better, but KNN (and probably many other classification algorithms) beat both. So, why bother?
  


