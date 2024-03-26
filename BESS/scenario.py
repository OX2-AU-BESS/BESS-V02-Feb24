# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 17:36:08 2023
@ Author: SIMULATION
@ Revised/restructured: Mojtaba Jabbari Ghadi
"""
from    datetime   import datetime, timedelta
import  os

class Scenario:
    def __init__(self, scenario_params):
        self.start_timestamp            = scenario_params['start_timestamp'             ]
        self.overall_start_timestamp    = scenario_params['overall_start_time'          ]
        self.end_timestamp              = scenario_params['end_timestamp'               ]
        self.battery_SOC                = scenario_params['battery_SOC'                 ]
        self.target_SOC                 = scenario_params['target_SOC'                  ] 
        self.SoC_tolerance              = scenario_params['SoC_tolerance'               ]
        self.max_cycles                 = scenario_params['max_cycles'                  ]
        self.FCAS_occurance             = scenario_params['FCAS_occurance'              ]
        self.FCAS_MW_Participation_Reg  = scenario_params['FCAS_MW_Participation_Reg'   ]
        self.FCAS_MW_Participation_Cont = scenario_params['FCAS_MW_Participation_Cont'  ]
        self.LGC_price                  = scenario_params['LGC_price'                   ]
        self.max_FCAS_percent           = scenario_params['max_FCAS_percent'            ]
        self.data_source                = scenario_params['data_source'                 ]
        self.export_limits              = scenario_params['export_limits'               ]
    

#========================================================================================
# ================== Divide simulation period into monthly sub-periods ==================
def divide_period(start_date, end_date):
    # Parse start_date and end_date strings to datetime objects
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date   = datetime.strptime(end_date  , "%d/%m/%Y")
    
    # Initialize a list to store timestamps
    timestamps = []

    # Start iterating from start_date until end_date
    current_date = start_date
    while current_date <= end_date:
        # Determine the end of the current month
        end_of_month = current_date.replace(day=1) + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timedelta(days=1)
        
        # Adjust the end_of_month if it goes beyond the end_date
        if end_of_month > end_date:
            end_of_month = end_date
        
        # Add timestamp for the current month
        # timestamps.append((current_date.strftime("%d/%m/%Y"), (end_of_month+ timedelta(days=1)).strftime("%d/%m/%Y")))
        timestamps.append((current_date.strftime("%d/%m/%Y"), (end_of_month).strftime("%d/%m/%Y")))
        # Move to the next month
        current_date = end_of_month + timedelta(days=1)
    return timestamps


#========================================================================================
# ============== Creat directory for output folder======================================= 
def create_folder(directory):

    # Check if the parent folder "Output" already exists, otherwise Create it
    parent_directory = os.path.dirname(directory)
    if not os.path.exists(parent_directory):
        os.mkdir(parent_directory)

    # Check if the folder already exists, otherwise Create a new folder
    if not os.path.exists(directory       ):
        os.mkdir(directory       )