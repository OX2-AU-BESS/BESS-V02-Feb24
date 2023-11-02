# -*- coding: utf-8 -*- 
"""
Created on Tue Jun 13 10:06:13 2023

@author: 341510anla
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dati
from datetime import datetime
import time
import os
file="concatenated.csv"

#username="Esco-nas01"
data_path=r"C:\Users\341510anla\OneDrive - OX2\Data\18. Grid\BESS Model Remote\Basic BESS Inputs\Output\October-06 16_31_SANDIGO_IESS_230MW_4hr_Pay_TUOS_results\\"+file
df=pd.read_csv(data_path)

class year_summary_excel:
    def main(df): 
        
        mlf_gen=0.9519
        mlf_load=0.9716
        print("Applying MLF to BESS dispatch")
        df['bess_dsp_energy'] = np.where(df['bess_dsp_energy'] >= 0, df['bess_dsp_energy'] * mlf_gen, df['bess_dsp_energy'] * mlf_load)
        # year summary prints a pie chart of what portion each part of the revenue streams contributed over the year
        #print(summary_dict)
        df['timestamp'] = pd.to_datetime(df['timestamp'],format='%Y/%m/%d %H:%M:%S')
        df['year'] = df['timestamp'].dt.strftime('%Y')
        # apply MLF modifier if bess is charging or discharging at any one time.
        
        # create an empty dictionary for each unique month in the timestamp column
        year_rev_data = {}
        for year in df['year'].unique():
            year_word = f"{year}"
            year_rev_data[year_word] = {}

            # group data by month
        grouped = df.groupby(df["timestamp"].dt.year)
        years_lst = grouped.groups.keys()
        print("Retrieving Year summary data")
        excel_sum_dict={"Variable":["Wholesale revenue","Solar Revenue","Charging Cost","High Price Volatility","FCAS Regulation", "FCAS Contingency", "Energy Throughput - Discharge", "Energy Throughput - Charge", "Average Discharging Price", "Average Charging Price", "Total Net Revenue"],
                        "Units":["AUD$","AUD$", "AUD$", "AUD$", "AUD$","AUD$", "MWh", "MWh", "AUD$/MWh", "AUD$/MWh", "AUD$"]}
        for year in years_lst:
            bess_ws_rev=0
            solar_rev=0
            bess_hpv_rev=0
            bess_chg_cost=0
            bess_dchg_cost=0
            fcas_reg_rev=0
            fcas_cont_rev=0
            bess_dchg=0
            bess_chg=0
            avg_chg=0
            avg_dchg=0
            tot_bess_rev=0
            group = grouped.get_group(year)
            # collect values in the energy column wherein the value is higher than $300/MWhr
            for i in range(len(group)):
                value = group['RRP_energy'].iloc[i]
                if value >= 300:
                    bess_hpv_rev += value * group['bess_dsp_energy'].iloc[i]
                    solar_rev += value *group['solar_dsp_energy'].iloc[i]
            # collect values in the energy column wherein the value is less than $300/MWhr
                elif value < 300:
                    bess_ws_rev += value * group['bess_dsp_energy'].iloc[i]
                    solar_rev += value *group['solar_dsp_energy'].iloc[i]
                else:
                    pass
            # Charging costs
                chg_value = group['bess_dsp_energy'].iloc[i]
                if chg_value < 0:
                    bess_chg_cost += group['RRP_energy'].iloc[i] * chg_value
                elif chg_value > 0: 
                    bess_dchg_cost += group['RRP_energy'].iloc[i] * chg_value
                else:
                    pass
            # collect FCAS Contingency values            
                fcas_cont_rev+= ((group['RRP_raise6sec'].iloc[i]*group['raise6sec'].iloc[i])
                                 +(group['RRP_raise60sec'].iloc[i]*group['raise60sec'].iloc[i])
                                 +(group['RRP_raise5min'].iloc[i]*group['raise5min'].iloc[i])
                                 +(abs(group['RRP_lower6s'].iloc[i]*group['lower6s'].iloc[i]))
                                 +(abs(group['RRP_lower60s'].iloc[i]*group['lower60s'].iloc[i]))
                                 +(abs(group['RRP_lower5min'].iloc[i]*group['lower5min'].iloc[i]))
                                 )
                								

            # collect FCAS Regulation values
                fcas_reg_rev+=(group['RRP_raisereg'].iloc[i]*group['raisereg'].iloc[i]+group['RRP_lowerreg'].iloc[i]*abs(group['lowerreg'].iloc[i]))
            # Through put of BESS charge
                if group['bess_combined'].iloc[i] < 0:
                    bess_chg+= group['bess_combined'].iloc[i]*0.5
                    
            # Through put of BESS discharge
                elif group['bess_combined'].iloc[i] > 0:
                    bess_dchg+= group['bess_combined'].iloc[i]*0.5
                    
                else:
                    pass
            # average charging price
            avg_chg = bess_chg_cost/bess_chg
            # average discharging price
            avg_dchg = bess_dchg_cost/bess_dchg
            # Total Revenue. (Sum of the top 5)
            tot_bess_rev=bess_hpv_rev+bess_ws_rev+fcas_cont_rev+fcas_reg_rev
            
            excel_sum_dict[year]=[bess_ws_rev, solar_rev, bess_chg_cost,bess_hpv_rev,fcas_reg_rev,fcas_cont_rev,bess_dchg,bess_chg,avg_dchg,avg_chg,tot_bess_rev]
            print(str(year) + " Completed")
        save_df= pd.DataFrame(excel_sum_dict)
        save_df.sort_index(inplace=True)
        
        now = datetime.now()
        # Format current time as string in yyyymmdd - hhmm format
        formatted_time = now.strftime("%Y%m%d - %H%M")
        file_path=r"C:\Users\341510anla\OneDrive - OX2\Data\18. Grid\BESS Model Remote\Basic BESS Inputs\Excel Output"+r"\\"+formatted_time+"_"+ "SUNSSF_40MW_2hr.csv"
        print(file_path)
        save_df.to_csv(file_path,index=False)
year_summary_excel.main(df)           