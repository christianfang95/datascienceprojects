#Import required packages
import numpy as np
import pandas as pd
import plotly.graph_objects as go


#Import MSCI data
dat = pd.read_csv("chart.csv")
dat.head()

#Plot MSCI chart development
fig = go.Figure()
fig.add_trace(go.Scatter(x = dat["Date"], y = dat["MSCI World"],
                    mode = 'lines'))
fig.update_layout(title = 'Development of MSCI World',
                  yaxis_title = "Value in Index Points",
                  xaxis_title = "Time",
                  font = dict(family = "Helvetica", size = 12))

#Define class
class stock_returns:
  #Constructor
  def __init__(self, data, years = 30, inflation = 0, start_date = None, end_date = None):
    self.data = data
    self.years = years
    self.inflation = inflation
    self.start_date = start_date
    self.end_date = end_date
  
  #Loss probability function
  def loss_proportion(self, 
                      data = None, 
                      years = None, 
                      inflation = None, 
                      start_date = None, 
                      end_date = None):
    if data is None: 
        self.data = self.data 
    else:
       self.data = data
    if years is None:
        self.years = self.years
    else: 
      self.years = years
    if inflation is None:
        self.inflation = self.inflation
    else:
      self.inflation = inflation
    if start_date is None:
        self.start_date = self.start_date
    else:
      self.start_date = start_date
    if end_date is None:
        self.end_date = self.end_date
    else:
      self.end_date = end_date

    #Define intervals and empty list to hold resuls
    intervals = list(range(1, self.years + 1))
    probability_loss = []

    #delete rows in data that lie before start date
    if self.start_date is not None: 
      self.data = self.data[~(pd.to_datetime(self.data["Date"]) 
      < self.start_date)]
    #delete rows in data that lie after end date
    if self.end_date is not None: 
      self.data = self.data[~(pd.to_datetime(self.data["Date"]) 
      > self.end_date)]

    #Loop over all intervals and caculate the losses
    for i in intervals:
        #Define the length of the respective interval: number of years times 12 
        length_interval = 12 * i
        #Calculate how many intervals are possible
        max_interval = len(self.data) - length_interval
        #Initialize results list
        result = []
        #Segment data into intervals and store in results list
        for i in range(max_interval):
            res = self.data[i:i+length_interval]
            result.append(res)
        #Create array from results and reshape to 2d array
        arr = np.array(result)
        reshaped = arr.reshape(max_interval, length_interval* 2)
        #Delete date column
        reshaped = np.delete(reshaped, list(range(0, reshaped.shape[1], 2)), axis=1)
        #Transpose so that each individual time series is in its own column
        reshaped = reshaped.transpose()
        #Get starting value of each series
        startval = reshaped[:1,:]
        #Normalize the results. -> divide all values in the time series by the 
        #starting value and substract one, so that the values represent relative 
        #changes from the beginning of the time series. 
        norm = []
        for i in range(max_interval):
            norm.append((reshaped[:,i] / startval[0,i]) - 1)
        #Calculate in how many cases you made a loss 
        #(absolute and when taking inflation into account)

        #Create array
        array = np.array(norm)
        #Extract end values and store them in a data frame
        end_vals = array[:, -1]
        end_vals = pd.DataFrame(end_vals)
        #Absolute losses: when end value is lower than starting value
        loss_abs = end_vals.apply(lambda x : True
                    if x[0] < 0 else False, axis = 1)
        # Number of absolute losses: filter results
        num_loss_abs = len(loss_abs[loss_abs == True].index)
        #Probability/Proportion of absolute losses: divide number of time series 
        #in which a loss was incurred by number of time series
        prop_loss_abs = num_loss_abs / max_interval
        #Relative losses: when end value is lower than starting value 
        #plus inflation per year
        loss_inf = end_vals.apply(lambda x : True
                    if x[0] < ((1 + (self.inflation/100)) ** 
                               (length_interval / 12) - 1) 
                    else False, axis = 1)
        # Number of relative losses: filter results
        num_loss_inf = len(loss_inf[loss_inf == True].index)
        #Probability/Proportion of absolute losses
        prop_loss_inf = num_loss_inf / max_interval
        #Append results to list we defined outside of the loop.
        probability_loss.append([prop_loss_abs, prop_loss_inf])
        
    #Create a dataframe
    self.loss_frame = pd.DataFrame(probability_loss).reset_index().rename(
        {'index': 'Years', 0: 'Probability absolute loss', 
         1: 'Probability relative loss'}, axis=1)
  
  #Export frame
  def frame(self):
    return self.loss_frame

  #Define plot function
  def visualize(self, loss_frame = None):
    if loss_frame is None: 
        self.loss_frame = self.loss_frame 
    else:
       self.loss_frame = loss_frame

    fig = go.Figure()
    fig.add_trace(go.Scatter(x = self.loss_frame["Years"], 
                             y = self.loss_frame["Probability absolute loss"],
                             mode = 'lines',
                             name = 'Absolute loss'))
    fig.add_trace(go.Scatter(x = self.loss_frame["Years"], 
                             y = self.loss_frame["Probability relative loss"],
                             mode = 'lines',
                             name = 'Relative loss ' + '(taking inflation ' + 
                                    'into account)'))
    fig.update_layout(title='Probability of Incurring Losses When Investing ' + 
                      'in MSCI World, per Years Invested',
                      xaxis_title='Years',
                      yaxis_title='Proportion making losses',
                      font=dict(family="Helvetica", size=12))
    fig.update_layout(legend=dict(orientation="h",
                                  yanchor="bottom",
                                  y=1.02,
                                  xanchor="right",
                                  x=1))
    fig.show()


#Generate example
x = stock_returns(data = dat, inflation = 2, years = 30)
x.loss_proportion()
x.visualize()
