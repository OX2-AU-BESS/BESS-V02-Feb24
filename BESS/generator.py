# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 16:55:11 2023
Class containing information about the generator to be used in the optimisation
@ Author: Mervin
@ Revised/restructured: Mojtaba Jabbari Ghadi

"""
import os
import pandas as pd

class Generator:
    def __init__(self, Inputs):

        self.plant_max_MW           = Inputs['plant_max_MW'             ]
        self.plant_min_MW           = Inputs['plant_min_MW'             ]
        self.solar_MW_rating        = Inputs['solar_MW_rating'          ]
        self.bat_max_MW             = Inputs['bat_max_MW'               ]
        self.bat_min_MW             = Inputs['bat_min_MW'               ]
        self.bat_capacity           = Inputs['bat_capacity'             ]
        self.min_SOC                = Inputs['min_SOC'                  ]
        self.max_SOC                = Inputs['max_SOC'                  ]
        self.mlf_gen                = Inputs['marginal_loss_factor_gen' ]
        self.mlf_load               = Inputs['marginal_loss_factor_load']
        self.round_trip_efficiency  = Inputs['round_trip_efficiency'    ]
        self.solar_gen_profile_path = Inputs['InputFolderPath'          ] + "\\" + Inputs['solar_gen_profile']
        self.solar_gen_profile      = []
        self.bat_deg_profile        = Inputs['InputFolderPath'          ] + "\\" + Inputs['bat_deg_profile'  ]
        self.location               = Inputs['location'                 ]
        self.SOC                    = 0


    #========================================================================================
    # ============== Import solar generation ================================================         
    def load_solar_profile(self, time_resolution):       
        # ------ read the xlsx/csv file into a pandas dataframe -----------------------
        file_path = self.solar_gen_profile_path
        file_type = os  .path.splitext(file_path)[1]
        if file_type == '.xlsx':
            df = pd.read_excel(file_path)
        elif file_type == '.csv':
            df = pd.read_csv  (file_path)
        
        #  ------ create a datetime column from the month, day, and hour columns ------------
        df['datetime'] = pd.to_datetime(df["Year"].astype(str) + '-' +df['Month'].astype(str) + '-' + df['Day'].astype(str) + '-' + df['Hour'].astype(str), format='%Y-%m-%d-%H:%M')
        df             = df.drop(df.columns[:4], axis=1)
        
        #  ------ set the datetime column as the dataframe index ----------------------------
        df.set_index('datetime', inplace=True)
        
        if time_resolution == 30:
            df_resampled = df
        else:
            df_resampled = df.resample(f'{time_resolution}T').interpolate()
        
        self.solar_gen_profile=df_resampled


    #========================================================================================
    # ============== Set SOC directly (from 0 to 1) ========================================= 
    def set_SOC(self, SOC_percent):
        self.SOC=SOC_percent
        
        
        

