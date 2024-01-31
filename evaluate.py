from rps import *
import csv
import pandas as pd
import seaborn as sns


with open('file.csv', 'r') as file:
    df = pd.read_csv(file)

    df = df.groupby('tag')['val'].aggregate('sum')
    df.plot(x="tag", y="val", kind="bar") 

    plt.show() 

    print(df)