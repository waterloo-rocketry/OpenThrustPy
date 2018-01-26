import configparser


def writeSettingsToFile(ParserObject, SettingsPath, cfg):
    # Takes a dictionary of values and writes it to the settings file
    config = ParserObject
    
    config.set(
            "Rocket Dimensions",     
            "Oxidizer Tank Volume (L)",      
            cfg["ox_tank_vol_L"]
            )
    config.set(
            "Rocket Dimensions",     
            "Nozzle Throat Area (cm^2)",      
            cfg["noz_thr_area_cm2"]
            )
    config.set(
            "Rocket Dimensions",     
            "Nozzle Exit Area (cm^2)",        
            cfg["noz_ext_area_cm2"]
            )
    config.set(
            "Rocket Properties",     
            "Average Oxidizer/Fuel Ratio",   
            cfg["ox_fuel_ratio"]
            )
    config.set(
            "Rocket Properties",     
            "Ramp Up Time (s)",              
            cfg["ramp_up_s"]
            )
    config.set(
            "Rocket Properties",     
            "Ramp Down Time (s)",
            cfg["ramp_down_s"]
            )
    config.set(
            "Simulation Settings",   
            "Time Step (s)",                 
            cfg["time_step_s"]
            )
    config.set(
            "Simulation Settings",   
            "Convergence Weighting",         
            cfg["conv_weight"]
            )
    config.set(
            "Simulation Settings",   
            "Flow Model",                    
            cfg["flow_model"]
            )
    config.set(
            "Simulation Settings",   
            "Integeration Type",             
            cfg["integ_type"]
            )
    config.set(
            "Simulation Settings",   
            "Calculate Thrust Coefficient",  
            cfg["calc_thrust_coef"]
            )
    config.set(
            "Simulation Settings",   
            "C12",                           
            cfg["C12"]
            )
    
    with open(SettingsPath, 'w') as configfile:
        config.write(configfile)
    
    return True

def readSettingsFromFile(ParserObject):
    # Takes the settings file and generates a dictionary
    config = ParserObject
    try:
        rDim = config["Rocket Dimensions"]
        rProp = config["Rocket Properties"]
        simSet = config["Simulation Settings"]
        cfg = {}
        cfg["ox_tank_vol_L"]        = rDim["Oxidizer Tank Volume (L)"]
        cfg["noz_thr_area_cm2"]      = rDim["Nozzle Throat Area (cm^2)"]
        cfg["noz_ext_area_cm2"]      = rDim["Nozzle Exit Area (cm^2)"]
        cfg["ox_fuel_ratio"]        = rProp["Average Oxidizer/Fuel Ratio"]
        cfg["ramp_up_s"]            = rProp["Ramp Up Time (s)"]
        cfg["ramp_down_s"]          = rProp["Ramp Down Time (s)"]
        cfg["time_step_s"]          = simSet["Time Step (s)"]
        cfg["conv_weight"]          = simSet["Convergence Weighting"]
        cfg["flow_model"]           = simSet["Flow Model"]
        cfg["integ_type"]           = simSet["Integeration Type"]
        cfg["calc_thrust_coef"]     = simSet["Calculate Thrust Coefficient"]
        cfg["C12"]                  = simSet["C12"]
        return cfg
    except:
        print("Improperly formatted settings file, creating new one...")
        createNewSettingsFile("./settings.cfg")
        config.read("./settings.cfg")
        return readSettingsFromFile(config)
    

def createNewSettingsFile(settingsPath):
    config = configparser.ConfigParser()
    config["Rocket Dimensions"] = {}
    config["Rocket Properties"] = {}
    config["Simulation Settings"] = {}
    config["Rocket Dimensions"]["Oxidizer Tank Volume (L)"]         = "6.9"
    config["Rocket Dimensions"]["Nozzle Throat Area (cm^2)"]        = "3.82646"
    config["Rocket Dimensions"]["Nozzle Exit Area (cm^2)"]          = "18.1001"

    config["Rocket Properties"]["Average Oxidizer/Fuel Ratio"]      = "2.1"
    config["Rocket Properties"]["Ramp Up Time (s)"]                 = "4"
    config["Rocket Properties"]["Ramp Down Time (s)"]               = "6"

    config["Simulation Settings"]["Time Step (s)"]                  = "0.05"
    config["Simulation Settings"]["Convergence Weighting"]          = "0.2"
    config["Simulation Settings"]["Flow Model"]                     = "2"
    config["Simulation Settings"]["Integeration Type"]              = "2"
    config["Simulation Settings"]["Calculate Thrust Coefficient"]   = "False"
    config["Simulation Settings"]["C12"]                            = "2.23"

    with open(settingsPath, 'w') as configfile:
        config.write(configfile)

"""
# Sample code to create parser, read file, write to file, 
#     and generate a default settings file.
settingsPath = "./settings.cfg"
Parser = configparser.ConfigParser()
Parser.read(settingsPath)        
a = readSettingsFromFile(Parser)
print(a)
print("\n\nChanging values")
cfg = {
       'ox_tank_vol_L': '18.4', 
       'noz_thr_area_cm2': '6.98123', 
       'noz_ext_area_cm2': '40.1231', 
       'ox_fuel_ratio': '6.5', 
       'ramp_up_s': '6', 
       'ramp_down_s': '9', 
       'time_step_s': '0.01', 
       'conv_weight': '0.1', 
       'flow_model': '2', 
       'integ_type': '2', 
       'calc_thrust_coef': 'True', 
       'C12': '4.51'}
writeSettingsToFile(Parser, settingsPath, cfg)
Parser.read(settingsPath)
b = readSettingsFromFile(Parser)
print(b)
print("\n\nGenerating default settings file")
createNewSettingsFile(settingsPath)
Parser.read(settingsPath)
c = readSettingsFromFile(Parser)
print(c)
"""