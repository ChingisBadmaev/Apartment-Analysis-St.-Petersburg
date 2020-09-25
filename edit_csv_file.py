import csv
import pandas as pd
import numpy as np

df = pd.read_csv('house.csv', encoding='cp1251')
DataF = pd.read_csv('UPDATE_HOUSE.csv', encoding='cp1251')
# remove unnecessary
df['Price'] = df['Price'].apply(lambda x: x[:-4])
df['Metro distance'] = df['Metro distance'].apply(lambda x: str(x)[:-3])

Temp = df['Floor'].apply(lambda x: str.split(x, '/'))
df['Floor'] = Temp.apply(lambda x: x[0])
df['Max Floor'] = Temp.apply(lambda x: x[1])
df.to_csv('UPDATE_HOUSE.csv', index=False)
