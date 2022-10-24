import numpy as np

#population size
population = 8000000
#Number of carriers
carriers = 500
#Room size
room = 1000

#Probability of having at least one positive person
prob = 1 - np.power((1- (carriers / population)), room)

