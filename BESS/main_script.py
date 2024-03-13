# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 17:03:55 2023

Main script in which we define the generator and scenario for which we woudl like to estimate the revenue.

@ Author: Mervin
@ Revised/restructured: Mojtaba Jabbari Ghadi
"""
import datetime                            as dt
import multiprocessing
import os
import time
import pandas                              as pd
import dispatch_optimiser
import Import_Inputs
from   dispatch_optimiser import dispatch_optimiser
from   generator          import Generator as gen
from   scenario           import Scenario  as scn  

#========================================================================================
# ============== Calculate the 1st day of the next month ================================ 
def first_day_of_next_month(date_str):
    # Assuming the date is in the format "dd/mm/yyyy"
    day, month, year = map(int, date_str.split('/'))

    # Get the 1st day of the next month
    month = month + 1
    if month == 13: 
        month = 1
        year += 1
    return dt.datetime(year, month, day).strftime("%d/%m/%Y")
# ========================================================================================
from datetime import datetime, timedelta

def divide_period(start_date, end_date):
    # Parse start_date and end_date strings to datetime objects
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")
    
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
        timestamps.append((current_date.strftime("%d/%m/%Y"), (end_of_month+ timedelta(days=1)).strftime("%d/%m/%Y")))
        # timestamps.append((current_date.strftime("%d/%m/%Y"), (end_of_month).strftime("%d/%m/%Y")))
        # Move to the next month
        current_date = end_of_month + timedelta(days=1)

    
    return timestamps


#========================================================================================
# ============== Format month and year ================================================== 
def format_date(month, year):
    return dt.datetime(year, month, 1).strftime("%d/%m/%Y")

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


#========================================================================================
# ============== Parallel computation: Distributing computations on several cores ======= 
def run_script_multiprocessing(Inputs):
    # Get number of cores available: 
    # num_cores = multiprocessing.cpu_count()

    Multi_Processing= Inputs['Multi-Processing']

    # Example usage
    start_date = Inputs['start_timestamp'] # "2023-01-5"
    end_date   = Inputs['end_timestamp'] #  "2023-05-7"
    TimeStamps = divide_period(start_date, end_date)

        


    # month_year_combinations = [(month, year) for year in years   for month in months]

    if Multi_Processing:
        #  Multiprocessing
        num_cores = multiprocessing.cpu_count()
        # num_cores = 1
        print(f"Number of CPU cores: {num_cores}")
        pool      = multiprocessing.Pool(processes=num_cores)
                    
        # Generate all possible combinations of months and years
        pool. starmap(main_solve, [(StartDate, EndDate, Inputs) for StartDate, EndDate in TimeStamps])
        pool.close()
        pool.join()
    else:
        for StartDate, EndDate in TimeStamps:
            main_solve(StartDate, EndDate, Inputs)
            z=0  

#========================================================================================
# ============== Main solver of the algorithm =========================================== 
def main_solve(start_date, end_date, Inputs):   
    # start_date = format_date            (month, year) 
    # end_date   = first_day_of_next_month(start_date )
    
    # ------------- refer the script to the relevant documents --------------------
    # username = '341510anla' # Change this parameter to the username of the computer profile this script is being run on. sim mac: Esco-nas01, Angus PC: 10.0.0.210
    # path=r"C:\Users\{}\OneDrive - OX2\Data\18. Grid\BESS Model Remote\Basic BESS Inputs".format(username)+r"\\"
    # project_information = path + "Project information_template.xlsx"

    #  ------ Get input parameters from Project information.xlsx -------------------   
    # Inputs = Import_Inputs. Import_Data(folder_path)

    #  ------ Get input plant/scenario/solver parameters ---------------------------   
    plant_parameters={
                    'plant_max_MW'              :Inputs['plant_max_MW'              ],
                    'plant_min_MW'              :Inputs['plant_min_MW'              ],
                    'solar_MW_rating'           :Inputs['solar_MW_rating'           ],
                    'bat_max_MW'                :Inputs['bat_max_MW'                ],
                    'bat_min_MW'                :Inputs['bat_min_MW'                ],
                    'bat_capacity'              :Inputs['bat_capacity'              ],
                    'min_SOC'                   :Inputs['min_SOC'                   ],
                    'max_SOC'                   :Inputs['max_SOC'                   ],  
                    'marginal_loss_factor_gen'  :Inputs['marginal_loss_factor_gen'  ],
                    'marginal_loss_factor_load' :Inputs['marginal_loss_factor_load' ],
                    'round_trip_efficiency'     :Inputs['round_trip_efficiency'     ],
                    'location'                  :Inputs['location'                  ]+'1',
                    'bat_deg_profile'           :Inputs['InputFolderPath'] + "\\" + Inputs['bat_deg_profile'  ],
                    'solar_gen_profile'         :Inputs['InputFolderPath'] + "\\" + Inputs['solar_gen_profile'],
                    }
    
    scenario_parameters={
                    'start_timestamp'           :start_date                          , #scn_info['start_timestamp'], 1/10/2022
                    'end_timestamp'             :end_date                            , #scn_info['end_timestamp'], 30/06/2060 13:30
                    'overall_start_time'        :Inputs['overall_start_time'        ],
                    'battery_SOC'               :Inputs['battery_SOC'               ],
                    'target_SOC'                :Inputs['target_SOC'                ],
                    'SoC_tolerance'             :Inputs['SoC_tolerance'             ],
                    'max_cycles'                :Inputs['max_cycles'                ],            
                    'FCAS_occurance'            :Inputs['FCAS_occurrence'           ], #chance of an FCAS contingency event during any 30min time period, 0 < x <= 1.0
                    'FCAS_MW_Participation_Reg' :Inputs['FCAS_Participation_Reg'    ],
                    'FCAS_MW_Participation_Cont':Inputs['FCAS_Participation_Cont'   ], #% of battery SoC  
                    'LGC_price'                 :Inputs['LGC_price'                 ],
                    'max_FCAS_percent'          :Inputs['max_FCAS_percent'          ], #percentage limit defining what part of the battery can be used for FCAS
                    'data_source'               :'auto'                              , #automatically selects data based on time frame specified and data available
                    'export_limits'             :[]
                    }
    
    solver_parameters={
                    'optimisation_res'          :Inputs['optimisation_res'          ], #time interval lengt in minutes after which the dispatch otimisation to the end of intraday forecast period is carried out
                    'forecast_res'              :Inputs['forecast_res'              ], #time resolution of the forecast data to be used.
                    'forecast_data_path'        :Inputs['forecast_path'             ],
                    'revenue_method'            :Inputs['revenue_method'            ],
                    'Price_forecast_path'       :os.path.join(Inputs['InputFolderPath'], Inputs['Price forecast file']),
                    'output_directory'          :Inputs['output_directory'          ],
                    'forecast_Company'          :Inputs['forecast_Company'          ],
                      }
    
    #  ------ Get information of generator -----------------------------------------   
    generator = gen(plant_parameters)   

    #  ------ Get details of scenario ----------------------------------------------
    scenario  = scn(scenario_parameters)

    generator.set_SOC(scenario.battery_SOC)
    
    #  ------ optimisation ---------------------------------------------------------
    optimisation = dispatch_optimiser(generator, scenario, solver_parameters)  
    optimisation . optimise_dispatch()     
    
    #optimisation.save_results(r"C:\Users\SIMULATION\ESCO Pacific\ESCO - Data\36. Design\Tools\BatteryModel\Pythonscripts\PulpSolver_MervBranch\results")
    #report.init(output_directory, "full") #report object allows to specify type of report that we want. This can be refined quite a bit and can take more input parameters.
    #report.generate_report(generator, scn, optimisation.results)

#========================================================================================
# ============== Main algorithm body ==================================================== 
r"""
start_time = time.time()
folder_path = r"C:\Users\341510anla\OneDrive - OX2\Data\18. Grid\BESS Model Remote\Basic BESS Inputs\Output\\" + time.strftime("%B-%d %H_%M", time.localtime(start_time)) +"_45MW_2hr_results"
create_folder(folder_path)
main_solve(4, 2025,folder_path)
"""
if __name__ == "__main__":
    # months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # # duration of opt in years
    # dur   = 3
    # years = [] 
    # # Add the desired range of years
    # for i in range(0,dur):
    #     years.append(2025+i)
        
    Inputs = Import_Inputs. Import_Data()
    
    start_time        = time . time  ()
    current_directory = os   . getcwd()
    parent_directory  = os   . path. dirname(current_directory)
    OutPut_directory  = "Output"
    Output_SubFolder  = time . strftime("%B-%d %H_%M", time. localtime(start_time)) +" "+Inputs['Scenario Name']
    OutputFolder_path = os   . path. join (parent_directory, OutPut_directory, Output_SubFolder)
    Inputs['output_directory'] = OutputFolder_path

    create_folder(OutputFolder_path)
   
    df = run_script_multiprocessing(Inputs)
    #df.to_csv(folder_path+r"\\concatenated_results.csv",index=False)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The execution time: {execution_time}")


#"""