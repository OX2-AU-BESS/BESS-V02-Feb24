# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 17:36:08 2023

@author: SIMULATION
"""
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
    
    def print_params(self):
        print("start_timestamp:          ", self.start_timestamp        )
        print("end_timestamp:            ", self.end_timestamp          )
        print("battery_SOC:              ", self.battery_SOC            )
        print("target_SOC:               ", self.target_SOC             )
        print("max_cycles:               ", self.max_cycles             )
        print("FCAS_occurance:           ", self.FCAS_occurance         )
        print("FCAS_MW_Participation:    ", self.FCAS_MW_Participation  )
        print("LGC_price:                ", self.LGC_price              )
        print("max_FCAS_percent:         ", self.max_FCAS_percent       )
        print("data_source:              ", self.data_source            )
        print("export_limits:            ", self.export_limits          )

