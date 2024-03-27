# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 17:03:55 2023

Main script in which we define the generator and scenario for which we woudl like to estimate the revenue.

@ Author: Mervin
@ Revised/restructured: Mojtaba Jabbari Ghadi
"""
import datetime           as dt
import multiprocessing
import os
import time
import pandas             as pd
import dispatch_optimiser
import Import_Inputs
import scenario
import Massage_lists
import Data_Processing
from   dispatch_optimiser import dispatch_optimiser
from   generator          import Generator as gen
from   scenario           import Scenario  as scn  

#========================================================================================
# ============== Parallel computation: Distributing computations on several cores ======= 
def run_script_multiprocessing(Inputs):
    Multi_Processing= Inputs['Multi-Processing']

    # Example usage
    start_date   = Inputs['start_timestamp'] 
    end_date     = Inputs['end_timestamp'  ] 
    TimeStamps   = scenario.divide_period(start_date, end_date)
    Full_Results = pd.DataFrame()  
    if Multi_Processing:
        #  Multiprocessing
        num_cores = multiprocessing.cpu_count()
        # num_cores = 1
        print(f"Number of CPU cores: {num_cores}")
        pool      = multiprocessing.Pool(processes=num_cores)   

        # Run over all possible combinations of months and years
        Results=pool. starmap(main_solve, [(StartDate, EndDate, Inputs) for StartDate, EndDate in TimeStamps])
        pool.close()
        pool.join ()
        for result in Results:
            Full_Results=pd.concat([Full_Results, result], axis=0)

    else:
        for StartDate, EndDate in TimeStamps:
            result = main_solve(StartDate, EndDate, Inputs)
            Full_Results=pd.concat([Full_Results, result], axis=0)

    return Full_Results        




#========================================================================================
# ============== Main solver of the algorithm =========================================== 
def main_solve(start_date, end_date, Inputs):   

    #  ------ Get input plant/scenario/solver parameters ---------------------------   

    

    
    solver_parameters={
                    'optimisation_res'          :Inputs['optimisation_res'          ], #time interval lengt in minutes after which the dispatch otimisation to the end of intraday forecast period is carried out
                    'forecast_res'              :Inputs['forecast_res'              ], #time resolution of the forecast data to be used.
                    'forecast_data_path'        :Inputs['forecast_path'             ],
                    'revenue_method'            :Inputs['revenue_method'            ],
                    'Price_forecast_df'         :Inputs['Price_forecast_df'         ],
                    'output_directory'          :Inputs['output_directory'          ],
                    'foresight_period'          :Inputs['foresight_period'          ],
                    'Saving_period'             :Inputs['Saving_period'             ],
                      }
    
    #  ------ Get information of generator -----------------------------------------   
    generator = gen(Inputs)   

    #  ------ Get details of scenario ----------------------------------------------
    scenario  = scn(start_date, end_date, Inputs)

    #  ------ Get SOC of scenario --------------------------------------------------
    generator.set_SOC(scenario.battery_SOC)
    
    #  ------ optimisation ---------------------------------------------------------
    optimisation = dispatch_optimiser(generator, scenario, solver_parameters)  # Construct optimisation variable
    RunResult= optimisation . optimise_dispatch()     

    return RunResult

#========================================================================================
# ============== Main algorithm body ==================================================== 

if __name__ == "__main__":
        
    Scenarios_list = Import_Inputs. Import_Data()
    start_time  = time . time  ()

    if  not Scenarios_list:
        # List of scenarios is empty because
        # All scenarios are False in Project information.xlsx, row 'To run simulation' 
        Massage_lists.NoSelectedScenario()

    else:
        # There is at list one scenario to run
        for Inputs in Scenarios_list:
            current_directory = os   . getcwd()
            parent_directory  = os   . path. dirname(current_directory)
            OutPut_directory  = "Output"
            Output_SubFolder  = time . strftime("%B-%d %H_%M", time. localtime(start_time)) +" "+Inputs['Scenario Name']
            OutputFolder_path = os   . path. join (parent_directory, OutPut_directory, Output_SubFolder)
            Inputs['output_directory'] = OutputFolder_path
            scenario.create_folder(OutputFolder_path)
        
            Full_Results = run_script_multiprocessing(Inputs)
              
            # Save the csv file of full resul
            Data_Processing.save_results(Inputs, Full_Results)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The execution time: {execution_time}")

