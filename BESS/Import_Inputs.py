import pandas as pd
import os

def Import_Data():
    #  ------ Get directory for 'Project Information' file ------------------------
    Current_directory   = os.getcwd()
    Parent_directory    = os.path.dirname(Current_directory)
    Input_folder        = "Input"
    Input_templateXlsx  = r"Project information.xlsx"
    project_information = os.path.join(Parent_directory, Input_folder, Input_templateXlsx)

    #  ------ Get directory for 'Forecasted Price' file ---------------------------
    # output_directory    = folder_path
    Dispatch_results    = r"NSW1_dispatch_results.csv"
    forecast_path       = os.path.join(Parent_directory, Input_folder, Dispatch_results)

    #  ------ Get directory for 'Actual Price' file --------------------------------
    # Price_FolderFile    = r"Aurora\Australia 2022 Q3 (Low)_nsw"
    # actual_path         = os.path.join(Parent_directory, Input_folder)

    #  ------ Get directory for 'Input' folder -------------------------------------
    InputFolderPath     = os.path.join(Parent_directory, Input_folder)
                    
    #  ------ Importing data from different tabs of 'Project Information' file -----                
    Inputs  = pd.read_excel(project_information, sheet_name='Inputs')
    Inputs  = dict(zip(Inputs ['identifier'], Inputs ['value']))

    Inputs['InputFolderPath' ] = InputFolderPath
    Inputs['forecast_path'   ] = forecast_path
    
    # Inputs['output_directory'] = output_directory

    return Inputs


# def plant_scenario_solver_parameters(Inputs):
#     plant_parameters={
#                     'plant_max_MW'              :Inputs['plant_max_MW'              ],
#                     'plant_min_MW'              :Inputs['plant_min_MW'              ],
#                     'solar_MW_rating'           :Inputs['solar_MW_rating'           ],
#                     'bat_max_MW'                :Inputs['bat_max_MW'                ],
#                     'bat_min_MW'                :Inputs['bat_min_MW'                ],
#                     'bat_capacity'              :Inputs['bat_capacity'              ],
#                     'min_SOC'                   :Inputs['min_SOC'                   ],
#                     'max_SOC'                   :Inputs['max_SOC'                   ],  
#                     'marginal_loss_factor_gen'  :Inputs['marginal_loss_factor_gen'  ],
#                     'marginal_loss_factor_load' :Inputs['marginal_loss_factor_load' ],
#                     'round_trip_efficiency'     :Inputs['round_trip_efficiency'     ],
#                     'location'                  :Inputs['location'                  ]+'1',
#                     'bat_deg_profile'           :Inputs['InputFolderPath'] + "\\" + Inputs['bat_deg_profile'  ],
#                     'solar_gen_profile'         :Inputs['InputFolderPath'] + "\\" + Inputs['solar_gen_profile'],
#                     }
    
#     scenario_parameters={
#                     'start_timestamp'           :start_date                          , #scn_info['start_timestamp'], 1/10/2022
#                     'end_timestamp'             :end_date                            , #scn_info['end_timestamp'], 30/06/2060 13:30
#                     'overall_start_time'        :Inputs['overall_start_time'        ],
#                     'battery_SOC'               :Inputs['battery_SOC'               ],
#                     'target_SOC'                :Inputs['target_SOC'                ],
#                     'SoC_tolerance'             :Inputs['SoC_tolerance'             ],
#                     'max_cycles'                :Inputs['max_cycles'                ],            
#                     'FCAS_occurance'            :Inputs['FCAS_occurrence'           ], #chance of an FCAS contingency event during any 30min time period, 0 < x <= 1.0
#                     'FCAS_MW_Participation_Reg' :Inputs['FCAS_Participation_Reg'    ],
#                     'FCAS_MW_Participation_Cont':Inputs['FCAS_Participation_Cont'   ], #% of battery SoC  
#                     'LGC_price'                 :Inputs['LGC_price'                 ],
#                     'max_FCAS_percent'          :Inputs['max_FCAS_percent'          ], #percentage limit defining what part of the battery can be used for FCAS
#                     'data_source'               :'auto'                              , #automatically selects data based on time frame specified and data available
#                     'export_limits'             :[]
#                     }
    
#     solver_parameters={
#                     'optimisation_res'          :Inputs['optimisation_res'          ], #time interval lengt in minutes after which the dispatch otimisation to the end of intraday forecast period is carried out
#                     'forecast_res'              :Inputs['forecast_res'              ], #time resolution of the forecast data to be used.
#                     'forecast_data_path'        :Inputs['forecast_path'             ],
#                     'revenue_method'            :Inputs['revenue_method'            ],
#                     'actual_data_path'          :os.path.join(Inputs['InputFolderPath'], Inputs['actual_data_path']),
#                     'output_directory'          :Inputs['output_directory'          ],
#                       }
    
#     return plant_parameters, scenario_parameters, solver_parameters
   