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
    def __init__(self, gen_params):
        self.plant_max_MW           = gen_params['plant_max_MW'             ]
        self.plant_min_MW           = gen_params['plant_min_MW'             ]
        self.solar_MW_rating        = gen_params['solar_MW_rating'          ]
        self.bat_max_MW             = gen_params['bat_max_MW'               ]
        self.bat_min_MW             = gen_params['bat_min_MW'               ]
        self.bat_capacity           = gen_params['bat_capacity'             ]
        self.min_SOC                = gen_params['min_SOC'                  ]
        self.max_SOC                = gen_params['max_SOC'                  ]
        self.mlf_gen                = gen_params['marginal_loss_factor_gen' ]
        self.mlf_load               = gen_params['marginal_loss_factor_load']
        self.round_trip_efficiency  = gen_params['round_trip_efficiency'    ]
        self.solar_gen_profile_path = gen_params['solar_gen_profile'        ]
        self.solar_gen_profile      = []
        self.bat_deg_profile        = gen_params['bat_deg_profile'          ]
        self.location               = gen_params['location'                 ]
        self.SOC                    = 0


    #========================================================================================
    # ============== charge battery by a set amount of MWh ==================================    
    def charge(self, MWh):
        if MWh>=0:
            self.SOC=self.SOC+MWh*(1-((1-self.round_trip_efficiency)/2.0))/self.bat_capacity
        else:
            self.SOC=self.SOC+MWh*(1+((1-self.round_trip_efficiency)/2.0))/self.bat_capacity


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
    # ============== discharge battery system by a set amount of MWh ========================         
    def discharge(self, MWh):
        if MWh>=0:
            self.SOC=self.SOC-MWh*(1+((1-self.round_trip_efficiency)/2.0))/self.bat_capacity
        else:
            self.SOC=self.SOC-MWh*(1-((1-self.round_trip_efficiency)/2.0))/self.bat_capacity


    #========================================================================================
    # ============== Set SOC directly (from 0 to 1) ========================================= 
    def set_SOC(self, SOC_percent):
        self.SOC=SOC_percent


    #========================================================================================
    # ============== Printing the parameters ================================================        
    def print_params(self):
        print("plant_max_MW:     "      , self.plant_max_MW         )
        print("plant_min_MW:     "      , self.plant_min_MW         )
        print("solar_MW_rating:  "      , self.solar_MW_rating      )
        print("bat_max_MW:       "      , self.bat_max_MW           )
        print("bat_min_MW:       "      , self.bat_min_MW           )
        print("bat_capacity:     "      , self.bat_capacity         )
        print("min_SOC:          "      , self.min_SOC              )
        print("max_SOC:          "      , self.max_SOC              )
        print("round_trip_efficiency: " , self.round_trip_efficiency)
        print("solar_gen_profile:"      , self.solar_gen_profile    )
        print("location:         "      , self.location             )    
        print("SOC:              "      , self.SOC                  )

        
        
        

