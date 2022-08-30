#Import required packages
import numpy as np
import pandas as pd
import plotly.express as px

#Set global parameters
P = 0 # The Starting Principal
r = 0.05 # The Annual Interest Rate to Compound On 7%
t = 30 # The Number of Years to Compound
M = 600 # Monthly Contribution Amount

#Compound interest with monthly contributions
results = pd.DataFrame(columns = ['Month', 'Invested', 'Value'])

for i in range(1, t * 12 + 1):
  Month = i
  Invested = P + (M * i)
  if r == 0.00: 
    Value = Invested
  else:
    Value = P * ((1 + (r / 12)) ** i) + M * ((((1 + r / 12) ** (i + 1)) - (1 + (r / 12))) / (r / 12))
  results =  results.append({'Month': Month, 'Invested': Invested, 'Value': Value}, ignore_index = True)

#plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=results["Month"], y=results["Invested"],
                    mode='lines',
                    name='Invested Capital'))
fig.add_trace(go.Scatter(x=results["Month"], y=results["Value"],
                    mode='lines',
                    fill='tonexty',
                    name='Value of Investment'))
fig.update_layout(title='Compound Interest',
                   xaxis_title='Months',
                   yaxis_title='Amount',
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

#Simulate different interest rates

rates = list(np.arange(0.010, 0.110, 0.010))
rates_res = pd.DataFrame(columns = ['Rate', 'Month', 'Invested', 'Value'])
for j in range(len(rates)):
    for i in range(1, t * 12 + 1):
        Month = i
        Invested = P + (M * i)
        if rates[j] == 0: 
            Value = Invested
        else:
         Value = P * ((1 + (rates[j] / 12)) ** i) + M * ((((1 + rates[j] / 12) ** (i + 1)) - (1 + (rates[j] / 12))) / (rates[j] / 12))
        rates_res =  rates_res.append({'Rate': rates[j], 'Month': Month, 'Invested': Invested, 'Value': Value}, ignore_index = True)

#Plot
fig = px.line(rates_res, x = rates_res["Month"], y = rates_res["Value"],
                    color = "Rate",
                    color_discrete_sequence=px.colors.sequential.Plasma)
fig.show()
fig.update_layout(title='Value of Investment, by annual interest rate',
                   xaxis_title='Months',
                   yaxis_title='Amount',
                   font=dict(
        family="Helvetica",
        size=12
    ))


# Simulate different amounts

amounts = list(range(100, 1000, 100))
res = pd.DataFrame(columns = ['Contribution', 'Month', 'Invested', 'Value'])
for j in range(len(amounts)):
    for i in range(1, t * 12 + 1):
        Month = i
        if r == 0: 
            Value = Invested
        else:
            Value = P * ((1 + (r / 12)) ** i) + amounts[j] * ((((1 + r / 12) ** (i + 1)) - (1 + (r / 12))) / (r / 12))
        Invested = P + (amounts[j] * i)
        res =  res.append({'Contribution': amounts[j], 'Month': Month, 'Invested': Invested, 'Value': Value}, ignore_index = True)

#
fig = px.line(res, x = res["Month"], y = res["Value"],
                    color = "Contribution",
                    color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_layout(title=str('Value of investment at ' + str(r * 100) + '% interest, per monthly contribution amount'),
                   xaxis_title='Months',
                   yaxis_title='Amount',
                   font=dict(
        family="Helvetica",
        size=12
    ))
