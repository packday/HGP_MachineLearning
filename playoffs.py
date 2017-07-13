
import numpy as np
import pandas as pd
import visuals as vs
import utils
from IPython.display import display

#Load data
file = 'resources/data/players_stats.csv'
data = pd.read_csv(file)

#Separate label from data
labels = data['Playoffs']
data = data.drop('Playoffs', axis = 1)

#graph data
vs.playoff_stats(data, labels, 'Games Played')

