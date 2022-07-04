import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

filename = 'test.csv'
directory = r'C:\Users\diamo\OneDrive\Desktop\Programming Assignment\Simulation_Results'


results = pd.read_csv(open(os.path.join(directory, filename)), names = [x for x in range(0,10)])
results['average'] = results.mean(axis=1)
pd.set_option('display.max_columns', None)
sorted = results.sort_values(by=['average'], ascending=False)
print(sorted.head(15))
