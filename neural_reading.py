# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt

# Read BCI data as a DataFrame
data = pd.read_csv('OpenBCI-R-ARM-M-RAW-2023-12-13_14-49-07.txt', delimiter=',', skiprows=4)

#print(data.columns)
column_data = data[' Timestamp']
f_row = data.iloc[1]
print(data.at[1, ' Timestamp'])

def main():
    
    #required variable definitions
    temp = 0.0
    avg1 = 0.0
    avg2 = 0.0
    avg3 = 0.0
    avg4 = 0.0
    avg5 = 0.0
    avg6 = 0.0
    avg7 = 0.0
    avg8 = 0.0
    avg9 = 0.0
    counter = 0
    xcount = 0.0
    
    #   plot
    plt.ion()
    fig, ax = plt.subplots(figsize=(10,6))
    
    #data array declarations
    x_data = []  
    y_data1 = []  
    y_data2 = []  
    y_data3 = []
    y_data4 = []
    y_data5 = []
    y_data6 = []
    y_data7 = []
    y_data8 = []
    

    #line and legend declaration
    line1, = ax.plot(x_data, y_data1, label='Channel 0')
    line2, = ax.plot(x_data, y_data2, label='Channel 1')
    line3, = ax.plot(x_data, y_data3, label='Channel 2')
    line4, = ax.plot(x_data, y_data4, label='Channel 3')
    line5, = ax.plot(x_data, y_data5, label='Channel 4')
    line6, = ax.plot(x_data, y_data6, label='Channel 5')
    line7, = ax.plot(x_data, y_data7, label='Channel 6')
    line8, = ax.plot(x_data, y_data8, label='Channel 7')
    ax.legend()

    #file call
    file_path = r'C:\Users\user\Documents\FUTECH\OpenBCI-RAW-2023-10-27_16-31-04.txt'
    
    #try loop
    try:
        with open(file_path, 'r') as data_file:
            while True:
                line = data_file.readline()
                if not line:
                    break
                
                #creates array of data from line in file using ', ' as a seperator
                data_points = line.split(', ')
                
                #checks if line is full data
                if len(data_points) < 8:
                    continue
                
                #Compares file sample # to amount of times run
                #index 0 in file should count up from zero if that is not true, skip line
                if float(data_points[0]) < temp:
                    continue
                elif float(data_points[0]) != temp:
                    temp += 1
                    continue
                elif temp >= 255:
                    temp = 0
                else:
                    temp += 1 

                #uses loop to convert data into float
                #also checks if value is not convertible and error messages
                for j in range(9):

                    if j < len(data_points):
                        try:
                            data_points[j] = float(data_points[j])
                        except ValueError:
                            print(f"Error converting {data_points[j]} to float at index {j}") 
                
                #adds each value into a varaible for averaging later
                avg2 = avg2 + data_points[1]
                avg3 = avg3 + data_points[2]
                avg4 = avg4 + data_points[3]
                avg5 = avg5 + data_points[4]
                avg6 = avg6 + data_points[5]
                avg7 = avg7 + data_points[6]
                avg8 = avg8 + data_points[7]
                avg9 = avg9 + data_points[8]
                
                #counts runs
                counter += 1

                #if program has gone through 255 runs, begins to average and update graph 
                #based on 250Hz per half second rate of cyton board
                if counter >= 255:

                    #averages
                    avg2 = avg2/255.0
                    avg3 = avg3/255.0
                    avg4 = avg4/255.0
                    avg5 = avg5/255.0
                    avg6 = avg6/255.0
                    avg7 = avg7/255.0
                    avg8 = avg8/255.0
                    avg9 = avg9/255.0

                    #updating data arrays with averages and increases x by 0.5 for half seconds
                    x_data.append(xcount)
                    xcount += 0.5
                    y_data1.append(avg2)
                    y_data2.append(avg3)
                    y_data3.append(avg4)
                    y_data4.append(avg5)
                    y_data5.append(avg6)
                    y_data6.append(avg7)
                    y_data7.append(avg8)
                    y_data8.append(avg9)

                    #sets graph values to updated values
                    line1.set_data(x_data, y_data1)
                    line2.set_data(x_data, y_data2)
                    line3.set_data(x_data, y_data3)
                    line4.set_data(x_data, y_data4)
                    line5.set_data(x_data, y_data5)
                    line6.set_data(x_data, y_data6)
                    line7.set_data(x_data, y_data7)
                    line8.set_data(x_data, y_data8)

                    #graph safeguards
                    ax.set_ylim(0.0, 150000.0)
                    ax.set_xlim(0.0,20.0)
                    fig.canvas.flush_events()
                   
                    #delay
                    time.sleep(1)

                    #reset counters and average variables for repeating the process
                    counter = 0
                    avg2 = 0.0
                    avg3 = 0.0
                    avg4 = 0.0
                    avg5 = 0.0
                    avg6 = 0.0
                    avg7 = 0.0
                    avg8 = 0.0
                    avg9 = 0.0    
                    
    #error failsafes
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

#declarations 
if __name__ == '__main__':
    plt.close('all')
    main()
