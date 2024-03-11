# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:44:52 2023

@ Author: SIMULATION
@ Revised/restructured: Mojtaba Jabbari Ghadi

"""
import os
import pandas as pd

username="10.0.0.210"
header = ['SETTLEMENTDATE','REGIONID','RRP','RAISE6SECRRP','RAISE60SECRRP','RAISE5MINRRP','RAISEREGRRP','LOWER6SECRRP','LOWER60SECRRP','LOWER5MINRRP','LOWERREGRRP']
regions = ["NSW1","QLD1","SA1","TAS1","VIC1"]
suffix = ["PUBLIC_DVD_DISPATCHPRICE","PUBLIC_DVD_PREDISPATCHPRICE_D"]
path=r"\\{}\sim-live\1. Grid\1. Data\BatteryModel\Nemweb_data\nemweb_SQLLoader_data".format(username)
def retrieve(path,header):
    
    df_dict={}  
    dfs=[]
    r=0
    for i in os.listdir(path):
        
        df_name = "df{}".format(r)
        df=pd.read_csv(path+ r"\\"+ i, usecols = header, skiprows = 1, error_bad_lines=False)
        df.drop(df.tail(1).index,inplace=True)
        locals()[df_name] = df
        dfs.append(locals()[df_name])
        r+=1
        df_end=pd.concat(dfs)
        df_end.reset_index(drop=True, inplace=True)
    return df_end
def dispatch(regions):
    print("yay")
            
def main():
    df_dict_set=[]
    df_dict_fore=[]
           
    for i in suffix:
        if i == suffix[0]:
            header = ['SETTLEMENTDATE','REGIONID','RRP','RAISE6SECRRP','RAISE60SECRRP','RAISE5MINRRP','RAISEREGRRP','LOWER6SECRRP','LOWER60SECRRP','LOWER5MINRRP','LOWERREGRRP']
        if i == suffix[1]:
            header = ['DATETIME','REGIONID','RRP','RAISE6SECRRP','RAISE60SECRRP','RAISE5MINRRP','RAISEREGRRP','LOWER6SECRRP','LOWER60SECRRP','LOWER5MINRRP','LOWERREGRRP']
        df = retrieve(path+r"\\"+i,header)
        
        if i == suffix[0]:
            for region in regions:
                
                index_names = df[df['REGIONID'] != region ].index
                df_temp=df.drop(index_names, inplace = False)
                df_temp.reset_index(drop=True,inplace=True)
                
                df_temp['SETTLEMENTDATE'] = pd.to_datetime(df_temp['SETTLEMENTDATE'])
                df_temp.set_index(df_temp['SETTLEMENTDATE'], inplace=True)
                df_30min_mean = df_temp.resample('30T').mean()
                df_30min_mean.insert(loc=0, column='REGIONID', value=region)
                
                df_dict_set.append(df_30min_mean)
                
        if i == suffix[1]:
            for region in regions:
                
                index_names = df[df['REGIONID'] != region ].index
                df_temp=df.drop(index_names, inplace = False)
                df_temp.reset_index(drop=True,inplace=True)
                df_temp.rename(inplace=True,columns={"DATETIME":'SETTLEMENTDATE'})
                df_temp['SETTLEMENTDATE'] = pd.to_datetime(df_temp['SETTLEMENTDATE'])
                df_temp.set_index(df_temp['SETTLEMENTDATE'], inplace=True)
                df_30min_mean = df_temp.resample('30T').mean()
                df_30min_mean.insert(loc=0, column='REGIONID', value=region)
                
                df_dict_fore.append(df_30min_mean)
                
    return df_dict_set, df_dict_fore
            
#main()
        

