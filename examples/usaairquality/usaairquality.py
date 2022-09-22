from pathlib import Path

import numpy as np
import pandas as pd
import requests

from pandas_profiling.utils.cache import cache_file
from pandas_profiling.visualisation.plot import timeseries_heatmap
from pandas_profiling import ProfileReport

if __name__ == '__main__':
    
    file_name = cache_file(
        "pollution_us_2000_2016.csv",
        "https://query.data.world/s/mz5ot3l4zrgvldncfgxu34nda45kvb",
    )

    df = pd.read_csv(file_name, index_col=[0])
    
    #Prepare the dataset
    #We will only consider the data from Arizone state for this example
    df = df[df['State']=='Arizona']
    df['Date Local']=pd.to_datetime(df['Date Local'])
    
    #Plot the time heatmap distribution for the per entity time-series
    timeseries_heatmap(dataframe=df, entity_column='Site Num', sortby='Date Local')
    
    # Return the profile per station
    for group in df.groupby('Site Num'):
        print(f'Generating the profile for the Site num: {group[0]}')
        profile = ProfileReport(
            group[1],
            tsmode=True,
            sortby="Date Local",
            title=f"Air Quality profiling - Site Num: {group[0]}"
        )

        profile.to_file(f'Ts_Profile_{group[0]}.html')