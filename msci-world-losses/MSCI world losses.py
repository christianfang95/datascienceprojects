#Import required packages
import numpy as np
import pandas as pd
import plotly.graph_objects as go


#Import MSCI data
dat = pd.read_csv("chart.csv")

#Define intervals and empty list to hold resuls
intervals = list(range(1, 31))
probability_loss = []

#Loop over all intervals and caculate the losses
for i in intervals:
    #Define the length of the respective interval: number of years (i) times 12 (months)
    length_interval = 12 * i
    #Calculate how many intervals are possible
    max_interval = len(dat) - length_interval
    #Calculate the intervals that will be examined. Results will be stored in the results object.
    result = []
    for i in range(max_interval):
        res = dat[i:i+length_interval]
        result.append(res)
    #This yields a 3d array. Let's reshape it to make it more readable
    arr = np.array(result)
    reshaped = arr.reshape(max_interval, length_interval* 2)
    #We can disregard the date columns
    reshaped = np.delete(reshaped, list(range(0, reshaped.shape[1], 2)), axis=1)
    #Transpose so that each individual time series is in its own column
    reshaped = reshaped.transpose()
    #Get starting value (i.e., value of the MSCI world at the beginning of each time series)
    startval = reshaped[:1,:]
    #Normalize the results. -> divide all values in the time series by the starting value and substract one,
    # so that the values represent relative changes from the beginning of the time series. 
    norm = []
    for i in range(max_interval):
        norm.append((reshaped[:,i] / startval[0,i]) - 1)
    #Calculate in how many cases you made a loss (absolute and when taking inflation into account)
    array = np.array(norm)
    #Extract end values and store them in a data frame
    end_vals = array[:, -1]
    end_vals = pd.DataFrame(end_vals)
    #Absolute losses: when end value is lower than starting value
    loss_abs = end_vals.apply(lambda x : True
                if x[0] < 0 else False, axis = 1)
    # Number of absolute losses: filter results
    num_loss_abs = len(loss_abs[loss_abs == True].index)
    #Probability/Proportion of absolute losses: divide number of time series in which a loss was incurred by number of time series
    prop_loss_abs = num_loss_abs / max_interval
    #Relative losses: when end value is lower than starting value plus 2% inflation per year
    loss_inf = end_vals.apply(lambda x : True
                if x[0] < (1.02 ** (length_interval / 12) - 1) else False, axis = 1)
    # Number of relative losses: filter results
    num_loss_inf= len(loss_inf[loss_inf == True].index)
    #Probability/Proportion of absolute losses
    prop_loss_inf = num_loss_inf / max_interval
    #Append results to list we defined outside of the loop.
    probability_loss.append([prop_loss_abs, prop_loss_inf])
    

#Create a dataframe
loss_frame = pd.DataFrame(probability_loss)
loss_frame = loss_frame.reset_index()
loss_frame = loss_frame.rename({'index': 'Years', 0: 'Probability absolute loss', 1: 'Probability relative loss'}, axis=1) 

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