"""
Created on 22/03/2024 

Implements pre-optimisation/post optimisation data processing

@ Revised/restructured: Mojtaba Jabbari Ghadi
"""
import time
import pandas as pd

from   datetime   import datetime

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NOTE                                    Pre-processing 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++






# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NOTE                                    Post-processing    
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ------------- Export all values of a variable into a list parameter ------------  
def List_dictionary (Variable):
    all_elements = []
    all_elements = [element for sublist in Variable for element in sublist]
    return all_elements   

# ------------- Select and name optimisation variable in form of a dataframe -----  
def SelectingNaming_OutputVariables(self):
    self.results=pd.DataFrame({
                            'Date Time'       : List_dictionary(self.timestamps          ),
                            'Bess_energy'     : List_dictionary(self.bess_dsp_energy     ), 
                            'Solar_Energy'    : List_dictionary(self.solar_dsp_energy    ),
                            'R6'              : List_dictionary(self.raise6s             ), 
                            'R60'             : List_dictionary(self.raise60s            ), 
                            'R5m'             : List_dictionary(self.raise5min           ), 
                            'Rreg'            : List_dictionary(self.raisereg            ), 
                            'L6'              : List_dictionary(self.lower6s             ), 
                            'L60'             : List_dictionary(self.lower60s            ), 
                            'L5m'             : List_dictionary(self.lower5min           ), 
                            'Lreg'            : List_dictionary(self.lowerreg            ),
                            'Bess_combined'   : List_dictionary(self.bess_combined_output), 
                            'SOC'             : List_dictionary(self.SOC_profile         ),

                            'RRP_energy'      : List_dictionary(self.foreRRP_energy      ),
                            'RRP_R6'          : List_dictionary(self.foreRRP_raise6s     ), 
                            'RRP_R60'         : List_dictionary(self.foreRRP_raise60s    ), 
                            'RRP_R5min'       : List_dictionary(self.foreRRP_raise5min   ), 
                            'RRP_Rreg'        : List_dictionary(self.foreRRP_raisereg    ), 
                            'RRP_L6'          : List_dictionary(self.foreRRP_lower6s     ), 
                            'RRP_L60'         : List_dictionary(self.foreRRP_lower60s    ), 
                            'RRP_L5min'       : List_dictionary(self.foreRRP_lower5min   ), 
                            'RRP_Lreg'        : List_dictionary(self.foreRRP_lowerreg    ),
                            'BESS Cap (MWh)'  : List_dictionary(self.bat_capacity        ),
                            })
    return self

# ------------- Saving results ---------------------------------------------------  
def save_results(Inputs, Full_Results):
    # Get current time
    Time_now = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    Full_Results.to_csv(Inputs['output_directory']+"\\"+" Full_Dispatch "+Time_now+" .csv", index=False)
    pass
