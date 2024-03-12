import pandas as pd
import os

def Import_Data(folder_path):
    #  ------ Get directory for 'Project Information' file ------------------------
    Current_directory   = os.getcwd()
    Parent_directory    = os.path.dirname(Current_directory)
    Input_folder        = "Input"
    Input_templateXlsx  = r"Project information_template.xlsx"
    project_information = os.path.join(Parent_directory, Input_folder, Input_templateXlsx)

    #  ------ Get directory for 'Forecasted Price' file ---------------------------
    output_directory    = folder_path
    Dispatch_results    = r"NSW1_dispatch_results.csv"
    forecast_path       = os.path.join(Parent_directory, Input_folder, Dispatch_results)

    #  ------ Get directory for 'Actual Price' file --------------------------------
    Price_FolderFile    = r"Aurora\Australia 2022 Q3 (Low)_nsw"
    # actual_path         = os.path.join(Parent_directory, Input_folder)

    #  ------ Get directory for 'Input' folder -------------------------------------
    InputFolderPath     = os.path.join(Parent_directory, Input_folder)
                    
    #  ------ Importing data from different tabs of 'Project Information' file -----                
    Inputs  = pd.read_excel(project_information, sheet_name='Inputs')
    Inputs  = dict(zip(Inputs ['identifier'], Inputs ['value']))

    Inputs['InputFolderPath' ] = InputFolderPath
    Inputs['forecast_path'   ] = forecast_path
    Inputs['output_directory'] = output_directory


    z=0

    return Inputs