import numpy as np

#population size
population = 9033999
#Number of carriers
carriers = (113*7)*10
#Room size
room = 100

#Probability of having at least one positive person
prob = 1 - np.power((1- (carriers / population)), room)

