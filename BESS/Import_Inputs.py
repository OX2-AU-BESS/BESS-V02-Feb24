import pandas as pd
import os
import datetime
import Import_Inputs

# ======================================================================================
# ================ structure import and export folder ==================================
def Import_Data():
    #  ------ Get directory for 'Project Information' file ------------------------
    Current_directory   = os.getcwd()
    Parent_directory    = os.path.dirname(Current_directory)
    Input_folder        = "Input"
    Input_templateXlsx  = r"Project information.xlsx"
    project_information = os.path.join(Parent_directory, Input_folder, Input_templateXlsx)

    #  ------ Get directory for 'Input' folder -------------------------------------
    InputFolderPath     = os.path.join(Parent_directory, Input_folder)

    #  ------ Import data from ScenarioManager tab of 'Project Information' file ---
    Scenario      = pd.read_excel(project_information, sheet_name='ScenarioManager')
    Scenario_List = dict(zip(Scenario ['Parameter'], Scenario ['Value']))

    Sce_digits    = [int(digit) for digit in Scenario_List['Scenarios list'].split(',')]

    inputs_list = []
    for scenario in Sce_digits:
                  
        #  ------ Import data from different tabs of 'Project Information' file --------                
        Inputs  = pd.read_excel(project_information, sheet_name=Scenario_List['Project Sheet'])
        Inputs  = dict(zip(Inputs ['Parameter'], Inputs [str(scenario)]))

        Inputs['InputFolderPath'    ] = InputFolderPath
        Inputs['forecast_path'      ] = os.path.join(Parent_directory, Input_folder, Inputs['forecast_data_path'])
        
        #  ------ Import price forecaset csv make it ready for simulation -------------                   
        Price_forecast_df             = pd.read_csv(os.path.join(Inputs['InputFolderPath'], Inputs['Price forecast file']))
        Price_forecast_df             = Import_Inputs.Reformat_Forecats_Prices(Price_forecast_df, Inputs['forecast_Company']) # Change name of columns in Aurora/Baringa price forecast 
        Inputs['Price_forecast_df'  ] = Price_forecast_df

        inputs_list.append(Inputs)


   
    return inputs_list


# ======================================================================================
# ================ Reformat forecasted price data of the third party ===================
def Reformat_Forecats_Prices(Price_forecast, data_input):
    if data_input == "Aurora":
        # Price_forecast.drop       (Price_forecast.index[0], inplace=True)
        # Price_forecast.reset_index(drop=True,inplace=True               )
        Price_forecast.rename     (inplace=True,columns={
                                'Time (UTC)'                     :"Timestamp"      ,
                                'Wholesale market price'         :'RRP'            ,
                                'Contingency raise - 6 seconds'  :'RAISE6SECRRP'   ,
                                'Contingency raise - 60 seconds' :'RAISE60SECRRP'  ,
                                'Contingency raise - 5 minutes'  :'RAISE5MINRRP'   ,
                                'Raise regulation'               :'RAISEREGRRP'    ,
                                'Contingency lower - 6 seconds'  :'LOWER6SECRRP'   ,
                                'Contingency lower - 60 seconds' :'LOWER60SECRRP'  ,
                                'Contingency lower - 5 minutes'  :'LOWER5MINRRP'   ,
                                'Lower regulation'               :'LOWERREGRRP'    })
        Price_forecast . drop       (index=Price_forecast.index[0], axis=0  , inplace=True)
        Price_forecast . reset_index(                             drop=True , inplace=True)

    elif data_input == "Baringa":
        Price_forecast.rename(inplace=True,columns={
                                'Period'                         :"Timestamp"      ,
                                'Wholesale (RRN)'                :'RRP'            ,
                                'RAISE6SEC'                      :'RAISE6SECRRP'   ,
                                'RAISE60SEC'                     :'RAISE60SECRRP'  ,
                                'RAISE5MIN'                      :'RAISE5MINRRP'   ,
                                'RAISEREG'                       :'RAISEREGRRP'    ,
                                'LOWER6SEC'                      :'LOWER6SECRRP'   ,
                                'LOWER60SEC'                     :'LOWER60SECRRP'  ,
                                'LOWER5MIN'                      :'LOWER5MINRRP'   ,
                                'LOWERREG'                       :'LOWERREGRRP'    })
    
    #  ------ Change the format of the first column (i.e.,Timestamp) to datetime-----------------
    Price_forecast['Timestamp'] = pd.to_datetime(Price_forecast['Timestamp'])
    if type(Price_forecast["Timestamp"][0]) == datetime:
        # Type is `datetime`, Handle accordingly
        pass
    else:
        # Type is string
        Price_forecast['Timestamp'] = pd.to_datetime(Price_forecast['Timestamp'],format="%d/%m/%Y %H:%M", dayfirst=True)
        pass   

    #  ------ Change the format of the nexts columns to float------------------------------------
    lst_columns= Price_forecast.columns[1:]
    lst_columns=['RRP','RAISE6SECRRP','RAISE60SECRRP','RAISE5MINRRP','RAISEREGRRP','LOWER6SECRRP','LOWER60SECRRP','LOWER5MINRRP','LOWERREGRRP']
    for i in lst_columns:
        Price_forecast[i] = Price_forecast[i].apply(lambda x: float(x))   

    #  --- Allocate Timestamp column values to index and remove Timestamp column ----------------
    Price_forecast . set_index  (Price_forecast["Timestamp"] , inplace=True,drop=True )
    Price_forecast . drop       ('Timestamp'                 , axis=1   , inplace=True)
            
    return Price_forecast


