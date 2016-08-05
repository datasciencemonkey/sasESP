# -*- coding: utf-8 -*-
"""
Created on Sun Apr 03 00:20:32 2016

@author: sagang
"""
import re,os
import random as np
import datetime,time
import csv
def get_Model_ID():
    """a simple random integer generator for models/number of cars - can
    be changed easily"""
    return np.randrange(1,10)

def get_time_stamp():
    """a simple time stamp generator """
    return re.sub('\..+','',str(datetime.datetime.now()))

#Set variables
opcode = 'i'
xyh='n'
counter=1

def set_car_variables(model_id):
    """arbitrarily sets base values for different models of cars"""
    Speed_OBD = 38.9 + (15 * (model_id/10.0))
    RPM = 756.25 + (25 *(model_id/10.0))
    Engine_load_pct=(np.randrange(7,10)/10.00)+ (np.randrange(1,9)*.01)
    Engine_Coolant_temp= 87 + (5 * model_id/10.0)
    CO2_Emissions_avg= 201.25 + np.randrange(1,100)
    GPS_Altitude= 149.9
    result_tuple = (('speed',Speed_OBD),('rpm',RPM),('engine_load',Engine_load_pct),
                    ('coolant_temp',Engine_Coolant_temp),('emissions',CO2_Emissions_avg),('altitude',GPS_Altitude))
    model_variable = dict((x,y) for x,y in result_tuple)
    return model_variable




def zsimulate(value,range_low,range_high,tolerance):
    if value < range_low:
        value = value + (float(np.randint(1,tolerance*100)) / 100)
    elif value > range_high:
        value = value + (float(np.randint(-tolerance*100,-1)) / 100)
    else:
        value = value + (float(np.randint(-tolerance*100,tolerance*100)) / 100)

    return value

last_speed = 0
last_rpm = 0
last_engine_load = 0
last_coolant_temp = 0
last_emissions = 0
last_altitude =0

#def inject_spike():

#remove the file if it exists - so its not always appending
try:
    os.remove('cars_data.csv')
except OSError:
    pass


while (counter <=100000):
    #Be careful with the number here - if a constant stream is needed
    #set the while condition to True - this will result infinite stream
    time.sleep(.20) #every 200 millisecond interval
    current_time = get_time_stamp()
    Model_ID= get_Model_ID()
    model_variable_dict = set_car_variables(Model_ID)
    model_variable_dict['speed'] = zsimulate(model_variable_dict['speed'],0,190,10)
    model_variable_dict['rpm'] = zsimulate(model_variable_dict['rpm'],0,3700,2)
    #model_variable_dict['engine_load'] = zsimulate(model_variable_dict['engine_load'],0,1,1)
    model_variable_dict['coolant_temp'] = zsimulate(model_variable_dict['coolant_temp'],45,105,1)
    model_variable_dict['emissions'] = zsimulate(model_variable_dict['emissions'],122,300,1)
    model_variable_dict['altitude'] = zsimulate(model_variable_dict['altitude'],145,400,1)

    if model_variable_dict['speed'] <= 0:
        model_variable_dict['speed'] = last_speed
    last_speed = model_variable_dict['speed']

    if model_variable_dict['rpm'] <= 0:
        model_variable_dict['rpm'] = 0
    last_rpm = model_variable_dict['rpm']

    if model_variable_dict['engine_load'] <= 0:
        model_variable_dict['engine_load'] = 0
    last_engine_load = model_variable_dict['engine_load']

    if model_variable_dict['coolant_temp'] <= 0:
        model_variable_dict['coolant_temp'] = 0
    last_coolant_temp = model_variable_dict['coolant_temp']

    if model_variable_dict['emissions'] <= 0:
        model_variable_dict['emissions'] = 0
    last_emissions = model_variable_dict['emissions']

    if model_variable_dict['altitude'] <= 0:
        model_variable_dict['altitude'] = 0
    last_altitude = model_variable_dict['altitude']
    row = opcode,xyh,str(current_time),counter,model_variable_dict['speed'],model_variable_dict['rpm'],model_variable_dict['engine_load'],model_variable_dict['coolant_temp'],model_variable_dict['emissions'],model_variable_dict['altitude'],Model_ID
#    print row
    with open('cars_data.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(row)
    counter= counter + 1
