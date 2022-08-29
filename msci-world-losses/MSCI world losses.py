import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

#IMport MSCI data
dat = pd.read_csv("chart.csv")

#Define intervals and empty list to hold resuls
probability_loss = []
intervals = list(range(1, 31))

#Loop over all intervals and caculate the losses
for i in intervals:
    length_interval = 12 * i
    #Calculate how many intervals are possible
    max_interval = len(dat) - length_interval
    #Calculate intervals
    result = []
    for i in range(max_interval):
        res = dat[i:i+length_interval]
        result.append(res)
    #This resulyts in a 3d array. Let's reshape it to make it more readable
    arr = np.array(result)
    reshaped = arr.reshape(max_interval, length_interval* 2)
    #we can disregard the date columns for now 
    reshaped = np.delete(reshaped, list(range(0, reshaped.shape[1], 2)), axis=1)
    #Transpose so that each individual time series is in its own column
    reshaped = reshaped.transpose()
    #Get starting value
    startval = reshaped[:1,:]
    #Loop over all rows
    norm = []
    for i in range(max_interval):
        norm.append((reshaped[:,i] / startval[0,i]) - 1)
    #Calculate in how many cases you made a loss (absolute and when taking inflation into account)
    #loss = np.array(shape=(0, max_interval))
    array = np.array(norm)
    #Extract 
    end_vals = array[:, -1]
    end_vals = pd.DataFrame(end_vals)
    loss_abs = end_vals.apply(lambda x : True
                if x[0] < 0 else False, axis = 1)
    num_loss_abs = len(loss_abs[loss_abs == True].index)
    loss_inf = end_vals.apply(lambda x : True
                if x[0] < (1.02 ** (length_interval / 12) - 1) else False, axis = 1)
    num_loss_inf= len(loss_inf[loss_inf == True].index)
    prop_loss_abs = num_loss_abs / max_interval
    prop_loss_inf = num_loss_inf / max_interval
    probability_loss.append([prop_loss_abs, prop_loss_inf])
    

#Create a dataframe
loss_frame = pd.DataFrame(probability_loss)
loss_frame = loss_frame.reset_index()
loss_frame = loss_frame.rename({'index': 'Years', 0: 'Probability absolute loss', 1: 'Probability relative loss'}, axis=1) 

#Plot using seaborn
fig, ax = plt.subplots()
ax.set(xlabel='Years', ylabel='Probability of making a loss', title = "Probability of Losses per Years Invested, in MSCI World, 1978-2022")
ax = sns.lineplot(data=loss_frame, x = "Years", y = "Probability absolute loss", legend = True)
ax1 = sns.lineplot(data=loss_frame, x = "Years", y = "Probability relative loss")
plt.legend(title = "Probability of Losses", labels=["Absolute","With inflation"])

#Plot using plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=loss_frame["Years"], y=loss_frame["Probability absolute loss"],
                    mode='lines',
                    name='Absolute loss'))
fig.add_trace(go.Scatter(x=loss_frame["Years"], y=loss_frame["Probability relative loss"],
                    mode='lines',
                    name='Relative loss ' +
                    '(taking inflation ' + 
                    'into account'))
fig.update_layout(title='Probability of Incurring Losses When Investing in MSCI World, per Years Invested',
                   xaxis_title='Years',
                   yaxis_title='Probability of making a loss',
                   font=dict(
        family="Helvetica",
        size=12
    ))
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
