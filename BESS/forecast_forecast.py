# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 14:22:59 2023

@ Author: Angus Lamin
@ Revised/restructured: Mojtaba Jabbari Ghadi

"""

import numpy as np
import pandas as pd
from scipy import stats

import matplotlib.pyplot as plt
import concacenate_data as cada
from datetime import datetime
import os

"""
The functionality of this code is to produce a dataset which would be representative of forecast forecast price data from forecast settlement data 
distributed by Aurora for power prices. 
An uncertainty distribution, calculated from the difference of historical forecast and settlement price data taken from AEMO
"""

def var_sta_dev(df,aurora_df): #add aurora_df later, this is what the upper and lower bound are applied to. 
    """
    This function computes the mean, standard deviation, and confidence interval for a given column in the input DataFrame
    using a 30-minute interval for each hour of the day.
    
    Args:
    df: pandas DataFrame containing timestamp and energy columns
    column: string specifying the name of the energy column to compute statistics for
    aurora_df: DataFrame containing long term forecast data, which the confidence interval is applied to create a  
    Raise regulation
            Lower regulation
            Contingency raise - 6 seconds
            Contingency lower - 6 seconds
            Contingency raise - 60 seconds
            Contingency lower - 60 seconds
            Contingency raise - 5 minutes
            Contingency lower - 5 minutes
    Returns:
    None (the function prints the computed statistics for each 5-minute interval)
    """
    #adjust aurora data to drop unnecessary rows, reset the index and change the data values to a float type. 
    
    # extract the hour and minute from the timestamp and create a new column with the format 'HH:MM'
    df["timestamp"] = pd.to_datetime(df.index)
    
    df['header'] = df["timestamp"].dt.strftime('%H:%M')
   
    df.index = pd.to_datetime(df.index)

    # Filter out rows with an index on 29th February
    
    date_index= aurora_df.index
    # create a list of headers with 30-minute intervals from '00:00' to '23:55'
    headers = pd.date_range('00:00', '23:30', freq='30min').strftime('%H:%M')
    lower_bound={}
    upper_bound={}
    lst_cols=['RRP','RAISE6SECRRP','RAISE60SECRRP','RAISE5MINRRP','RAISEREGRRP','LOWER6SECRRP','LOWER60SECRRP','LOWER5MINRRP','LOWERREGRRP']
    print("obtaining bounds")
    for i in lst_cols:
        newer_df=0
        new_df=0
        # pivot the DataFrame using the 'header' column as columns and the energy column as values
        new_df = pd.DataFrame(columns=headers)
        new_df = df.pivot(index=None, columns='header', values=[i])
        
        # drop any columns with NaN values and reset the index
        newer_df = pd.concat([new_df[c].dropna().reset_index(drop=True) for c in new_df.columns], axis=1)
        
        # compute the mean and standard deviation for each 30-minute interval
        std_df = newer_df.std()
        
        values = np.tile(std_df.values, len(date_index)//48 + 1)[:len(date_index)]
        mod_std_df = pd.DataFrame({'Standard Deviation': values}, index=date_index)
        std_df=mod_std_df['Standard Deviation']
        # conf_level can be used to select data close to the aurora profile or allow a more random variety of data to be produced. the lower the conf_level the more precise to the forecast settlement data the forecast forecast becomes.
        conf_level = 0.25
        t_value = stats.t.ppf((1 + conf_level) / 2, len(aurora_df[i]) - 1)
        
        #load Aurora data here into a data frame and applying an upper and lower bound to the data set. 
        lower_bound[i]=(aurora_df[i] - t_value * std_df / np.sqrt(len(newer_df.std()))).tolist() # lower bound of confidence level 
        upper_bound[i]=(aurora_df[i] + t_value * std_df / np.sqrt(len(newer_df.std()))).tolist() # upper bound of confidence level
    df_upper = pd.DataFrame.from_dict(upper_bound)
    df_upper.set_index(date_index, drop=True, inplace=True)
    
    df_lower = pd.DataFrame.from_dict(lower_bound)
    df_lower.set_index(date_index, drop=True, inplace=True)
    
    return df_upper, df_lower
     
def apply_randomiser(region,aurora_path,data_input,username):
    """
    Args: 
        'market': string of the Aurora Data set column which is required. Selected from: 
            Wholesale market price
            Raise regulation
            Lower regulation
            Contingency raise - 6 seconds
            Contingency lower - 6 seconds
            Contingency raise - 60 seconds
            Contingency lower - 60 seconds
            Contingency raise - 5 minutes
            Contingency lower - 5 minutes
    Returns: 
        Forecast Forecast DataFrame (unnamed): A vector of random values within the upper and lower bounds 
                                               based on the confidence level provided. this can be used to estimate revenue out to 
                                               Aurora data length.         

    """
    
    # generate timestamps from '2022-01-01' to '2023-12-31' with 5-minute or 30-minute frequency
    
    #### EXAMPLE of AURORA DATA Path required::::aurora_path =r"\\{}\sim-live\1. Grid\1. Data\BatteryModel\AuroraScripts\aurora_data\Australia 2022 Q2 (Low)_vic\aud2021-system-30m.csv".format(username)
   

    diff_path=r"\\{}\sim-live\1. Grid\1. Data\BatteryModel\Far Forecast Scripts\Working Folder\Forecast Forecast data\historical_AEMO_".format(username)+region+"_forecast&settlement_difference_df.csv"
    diff_df=pd.read_csv(diff_path, index_col=0)
    
    # ------  Modifying input forecast settlement data a workable common format-------
    aurora_df = pd.read_csv(aurora_path)
    
    
    if data_input == "aurora":
        aurora_df.drop(aurora_df.index[0], inplace=True)
        aurora_df.reset_index(drop=True,inplace=True)
        aurora_df.rename(inplace=True,columns={'Time (UTC)':"Timestamp",
                                "Wholesale market price":'RRP',
                             'Contingency raise - 6 seconds':'RAISE6SECRRP',
                             'Contingency raise - 60 seconds':'RAISE60SECRRP',
                             'Contingency raise - 5 minutes':'RAISE5MINRRP',
                             'Raise regulation':'RAISEREGRRP',
                             'Contingency lower - 6 seconds':'LOWER6SECRRP',
                             'Contingency lower - 60 seconds':'LOWER60SECRRP',
                             'Contingency lower - 5 minutes':'LOWER5MINRRP',
                             'Lower regulation':'LOWERREGRRP'})
    elif data_input == "baringa":
        aurora_df.rename(inplace=True,columns={'Period':"Timestamp",
                                "Wholesale (RRN)":'RRP',
                             'RAISE6SEC':'RAISE6SECRRP',
                             'RAISE60SEC':'RAISE60SECRRP',
                             'RAISE5MIN':'RAISE5MINRRP',
                             'RAISEREG':'RAISEREGRRP',
                             'LOWER6SEC':'LOWER6SECRRP',
                             'LOWER60SEC':'LOWER60SECRRP',
                             'LOWER5MIN':'LOWER5MINRRP',
                             'LOWERREG':'LOWERREGRRP'})

    print("Retrieving upper and lower bounds")
    # upper and lower bounds returns values differences that can be applied to the Aurora Market price.
    # Create a dictionary of forecast settlement (aurora data) and theoretical forecast forecast 
    lst_cols=['RRP','RAISE6SECRRP','RAISE60SECRRP','RAISE5MINRRP','RAISEREGRRP','LOWER6SECRRP','LOWER60SECRRP','LOWER5MINRRP','LOWERREGRRP']
    for i in lst_cols:
        aurora_df[i] = aurora_df[i].apply(lambda x: float(x))
    aurora_df['Timestamp'] = pd.to_datetime(aurora_df['Timestamp'],dayfirst=True, format="%Y/%m/%d %H:%M:%S")
    date_index = pd.date_range(start=aurora_df["Timestamp"].loc[0], end=aurora_df["Timestamp"].iat[-1], freq='30min')
    aurora_df.set_index(date_index, drop=True, inplace=True)
    aurora_df = aurora_df[~((aurora_df['Timestamp'].dt.month == 2) & (aurora_df['Timestamp'].dt.day == 29))]
    aurora_df.drop(labels="Timestamp",axis=1,inplace=False)
    
    # ---------  input data to a standard deviation function --------  
    df_upper, df_lower = var_sta_dev(diff_df,aurora_df)
    print("Retrieved upper and lower bounds")
    #--- a measure of how random the points will be from the previous number. Default set at 10% difference----
    rand_factor = 0.25
    # loop through each row of the dataframe
    result_dict={}
    for col in df_upper.columns:
        result_dict[col] = []
        prev_random_number = None  # Initialize previous random number
        for i in range(len(df_upper)):
            lower_bound = df_lower[col][i]
            upper_bound = df_upper[col][i]
            
            if prev_random_number is None:
                # For the first iteration, select a random number within the bounds
                random_number = np.random.uniform(lower_bound, upper_bound)
            else:
                # Calculate the lower and upper bounds based on the previous random number
                lower_limit = max(prev_random_number - ((upper_bound-lower_bound) * rand_factor), lower_bound)
                upper_limit = min(prev_random_number + ((upper_bound-lower_bound) * rand_factor), upper_bound)
                
                # Select a random number within the adjusted bounds
                random_number = np.random.uniform(lower_limit, upper_limit)
                
            # Update the previous random number
            prev_random_number = random_number
            
            # Add the random number to the result dictionary
            result_dict[col].append(random_number) 
            if i/len(df_upper) == 0.5:
                print(f"Completed {i} of {len(df_upper)} of {col} items")
        print(f"Completed {col} \n \n \n")
    
    results_df=pd.DataFrame(result_dict,columns=result_dict.keys())
    results_df.set_index(aurora_df.index, drop=True, inplace=True)
    results_df["Timestamp"]=results_df.index
    
    return results_df
"""
    # Get current time
    now = datetime.now()
    # Format current time as string in yyyymmdd - hhmm format
    formatted_time = now.strftime("%Y%m%d - %H%M")
    folder_name = formatted_time + os.path.basename(aurora_path)
    # combine the directory path and folder name to create the new folder path
    output_directory = r"\\10.0.0.210\sim-live\1. Grid\1. Data\BatteryModel\Far Forecast Scripts\Parallel Processing\forecast_forecast common"
    new_folder_path = os.path.join(output_directory, folder_name)

    # use the mkdir method to create the new folder
    os.mkdir(new_folder_path)
    
    #dataframes to CSV
    results_df.to_csv(new_folder_path+r"//"+"dataframe_"+"_dispatch_results.csv", index=True)
    print("yay")
"""  
    
#apply_randomiser(region="VIC1",data_input="aurora", aurora_path=r"\\10.0.0.210\sim-live\1. Grid\1. Data\BatteryModel\Far Forecast Scripts\aurora_data\Australia 2022 Q2 (Low)_vic\aud2021-system-30m.csv", username="10.0.0.210")   