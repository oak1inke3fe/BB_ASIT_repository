# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 08:54:35 2022

@author: oaklin keefe

This is Level 0 pipeline: taking quality controlled Level00 data, making sure there is enough
'good' data, aligning it to the wind (for applicable sensors) then despiking it (aka getting 
rid of the outliers), and finally interpolating it to the correct sensor sampling frequency. 
Edited files are saved to the Level 1 folder, in their respective "port" sub-folder as .csv 
files.                                                                                          

Input:
    .txt files per 20 min period per port from Level1_errorLinesRemoved and sub-port folder
Output:
    .csv files per 20 min period per port into LEVEL_1 folder
    
    
"""
#%%
import numpy as np
import pandas as pd
# from pandas import rolling_median
import os
# import matplotlib.pyplot as plt
import natsort
# import statistics
# import time
import math
# from scipy import interpolate
# import re
# import scipy.signal as signal
# import pickle5 as pickle
# os.chdir(r'E:\mNode_test2folders\test')
print('done with imports')

#%%

### function start
#######################################################################################
# Function for aligning the U,V,W coordinaes to the mean wind direction
def alignwind(wind_df):
    # try: 
    wind_df = wind_df.replace('NAN', np.nan)
    wind_df['u'] = wind_df['u'].astype(float)
    wind_df['v'] = wind_df['v'].astype(float)
    wind_df['w'] = wind_df['w'].astype(float)
    # wind_df = wind_df[(wind_df['u'] > -10)&(wind_df['u'] < 10)]
    Ub = wind_df['u'].mean()
    Vb = wind_df['v'].mean()
    Wb = wind_df['w'].mean()
    Sb = math.sqrt((Ub**2)+(Vb**2))
    beta = math.atan2(Wb,Sb)
    beta_arr = np.ones(len(wind_df))*beta
    alpha = math.atan2(Vb,Ub)
    alpha_arr = np.ones(len(wind_df))*alpha
    x1 = wind_df.index
    x = np.array(x1)
    Ur = wind_df['u']*math.cos(alpha)*math.cos(beta)+wind_df['v']*math.sin(alpha)*math.cos(beta)+wind_df['w']*math.sin(beta)
    Ur_arr = np.array(Ur)
    Vr = wind_df['u']*(-1)*math.sin(alpha)+wind_df['v']*math.cos(alpha)
    Vr_arr = np.array(Vr)
    Wr = wind_df['u']*(-1)*math.cos(alpha)*math.sin(beta)+wind_df['v']*(-1)*math.sin(alpha)*math.sin(beta)+wind_df['w']*math.cos(beta)     
    Wr_arr = np.array(Wr)
    T_arr = np.array(wind_df['T'])
    u_arr = np.array(wind_df['u'])
    v_arr = np.array(wind_df['v'])
    w_arr = np.array(wind_df['w'])

    # b = beta*180/math.pi
    # a = alpha*180/math.pi
    # df_abSbComponents = pd.DataFrame({'alpha':a, 'beta':b, 'Uhoriz_raw':Sb})
    df_aligned = pd.DataFrame({'base_index':x,'Ur':Ur_arr,'Vr':Vr_arr,'Wr':Wr_arr,'T':T_arr,'u':u_arr,'v':v_arr,'w':w_arr,'alpha':alpha_arr,'beta':beta_arr})

    return df_aligned
#######################################################################################
### function end
# returns: df_aligned (index, Ur, Vr, Wr, T, u, v, w, alpha, beta)
print('done with alignwind function')

#%%
### function start
#######################################################################################
# Function for interpolating the RMY sensor (freq = 32 Hz)
def interp_sonics123(df_sonics123):
    sonics123_xnew = np.arange(0, 38400)   # this will be the number of points per file based
    df_align_interp= df_sonics123.reindex(sonics123_xnew).interpolate(limit_direction='both')
    return df_align_interp
#######################################################################################
### function end
# returns: df_align_interp
print('done with interp_sonics123 simple function')
#%%
### function start
#######################################################################################
# Function for interpolating the Gill sensor (freq = 20 Hz)
def interp_sonics4(df_sonics4):
    sonics4_xnew = np.arange(0, 24000)   # this will be the number of points per file based
    df_align_interp_s4= df_sonics4.reindex(sonics4_xnew).interpolate(limit_direction='both')
    return df_align_interp_s4
#######################################################################################
### function end
# returns: df_align_interp_s4
print('done with interp_sonics4 function')
#%%
### function start
#######################################################################################
# Function for interpolating the paros sensor (freq = 16 Hz)
def interp_paros(df_paros):
    paros_xnew = np.arange(0, 19200)   # this will be the number of points per file based
    df_paros_interp = df_paros.reindex(paros_xnew).interpolate(limit_direction='both')
    return df_paros_interp
#######################################################################################
### function end
# returns: df_paros_interp
print('done with interp_paros function')
#%%
### function start
#######################################################################################
# Function for interpolating the sonics to the same frequency as the pressure heads (downsample to 16 Hz)
def interp_sonics2paros(df_despiked_sonics):
    sonic2paros_xnew = np.arange(0, 19200)   # this will be the number of points per file based
    df_sonic2paros_interp= df_despiked_sonics.reindex(sonic2paros_xnew).interpolate(limit_direction='both')
    return df_sonic2paros_interp
#######################################################################################
### function end
# returns: df_align_interp
print('done with interp_sonic2paros function')
#%%
### function start
#######################################################################################
# Function for interpolating the met sensor (freq = 1 Hz)
def interp_met(df_met):    
    met_xnew = np.arange(0, 1200)   # this will be the number of points per file based
    s5_df_met_interp= df_met.reindex(met_xnew).interpolate(limit_direction='both')
    
    return s5_df_met_interp
#######################################################################################
### function end
# returns: s5_df_met_interp
print('done with interp_met function')
#%%
### function start
#######################################################################################
# Function for interpolating the lidar sensor (freq = 20 Hz)
def interp_lidar(df_lidar):    
    lidar_xnew = np.arange(0, 24000)   # this will be the number of points per file based
    s7_df_interp= df_lidar.reindex(lidar_xnew).interpolate(limit_direction='both')
    return s7_df_interp
#######################################################################################
### function end
# returns: s7_df_interp
print('done with interp_lidar function')
#%%
# df_abSbComps_1 = pd.DataFrame(columns=['alpha','beta','Uhoriz_orig'])
# df_abSbComps_2 = pd.DataFrame(columns=['alpha','beta','Uhoriz_orig'])
# df_abSbComps_3 = pd.DataFrame(columns=['alpha','beta','Uhoriz_orig'])
# df_abSbComps_4 = pd.DataFrame(columns=['alpha','beta','Uhoriz_orig'])
filepath= r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved"
for root, dirnames, filenames in os.walk(filepath): #this is for looping through files that are in a folder inside another folder
    for filename in natsort.natsorted(filenames):
        file = os.path.join(root, filename)
        # colspecs_port123 = [(1, 7), (9, 14), (16, 21), (25, 29), (30, 32),(34,36)] #set the length of each column from text .dat file
        # colspecs_port4 = [(1,3), (4, 6), (7, 13), (14, 20), (21, 27),(28,34),(36,38)]
        if filename.startswith("mNode_Port1"):
            filename_only = filename[:-4]
            path_save = r"E:\ASIT-research\BB-ASIT\Level1_align-despike-interp\port1/"
            path_saveB = r'E:\ASIT-research\BB-ASIT\Level2_analysis\resample_sonic2paros/'
            s1_df = pd.read_csv(file, index_col=None, header = None) #read file into df
            s1_df.columns =['u', 'v', 'w', 'T', 'err_code','chk_sum'] #set column names to the variable
            s1_df = s1_df[['u', 'v', 'w', 'T',]]            
            s1_df['u']=s1_df['u'].astype(float) 
            s1_df['v']=s1_df['v'].astype(float)            
            s1_df['u']=-1*s1_df['u']
            s1_df['w']=-1*s1_df['w']
            # s1_df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
            if (len(s1_df)>=3000) & (s1_df['u'].isna().sum()<1000):                                    
                df_aligned = alignwind(s1_df) #perform align wind function
                # print('TRY, df_aligned worked')
                df_aligned['Ur'] = df_aligned['Ur'].apply(lambda x: np.nan if abs(x) > 31 else x) #despiking winds > 40kts
                df_aligned['Vr'] = df_aligned['Vr'].apply(lambda x: np.nan if abs(x) > 10 else x) #despiking v component
                df_aligned['Wr'] = df_aligned['Wr'].apply(lambda x: np.nan if abs(x) > 5 else x) #despiking w component
                # print('TRY, despike lines worked')
                df_align_interp = interp_sonics123(df_aligned) #interpolating to the sensor's frequency                       
                # print('TRY, interpolate worked')
                # df_align_interp.to_csv(path_save+str(filename_only)+'_1.csv') #saving the new aligned, despiked, and interpolated df as a .csv file                       
                df_sonic2paros_interp = interp_sonics2paros(df_aligned)
                # df_sonic2paros_interp.to_csv(path_saveB+str(filename_only)+'_1.csv')
            else:
                df_align_interp = pd.DataFrame(np.nan, index=[0,1], columns=['base_index','Ur','Vr','Wr','T','u','v','w','alpha','beta'])
                df_sonic2paros_interp = pd.DataFrame(np.nan, index=range(0,1), columns=['base_index','Ur','Vr','Wr','T','u','v','w','alpha','beta'])
            df_align_interp.to_csv(path_save+str(filename_only)+'_1.csv') #saving the new aligned, despiked, and interpolated df as a .csv file                       
            df_sonic2paros_interp.to_csv(path_saveB+str(filename_only)+'_1.csv')
            print('Port 1 ran: '+filename)
            
        elif filename.startswith("mNode_Port2"):
            filename_only = filename[:-4]
            path_save = r"E:\ASIT-research\BB-ASIT\Level1_align-despike-interp\port2/"
            path_saveB = r'E:\ASIT-research\BB-ASIT\Level2_analysis\resample_sonic2paros/'
            s2_df = pd.read_csv(file, index_col=None, header = None) #read file into df
            s2_df.columns =['u', 'v', 'w', 'T', 'err_code','chk_sum'] #set column names to the variable
            s2_df = s2_df[['u', 'v', 'w', 'T',]]
            s2_df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
            if (len(s2_df)>=3000) & (s2_df['u'].isna().sum()<1000):                                    
                df_aligned = alignwind(s2_df) #perform align wind function
                # print('TRY, df_aligned worked')
                df_aligned['Ur'] = df_aligned['Ur'].apply(lambda x: np.nan if abs(x) > 31 else x) #despiking winds > 40kts
                df_aligned['Vr'] = df_aligned['Vr'].apply(lambda x: np.nan if abs(x) > 10 else x) #despiking v component
                df_aligned['Wr'] = df_aligned['Wr'].apply(lambda x: np.nan if abs(x) > 5 else x) #despiking w component
                # print('TRY, despike lines worked')
                df_align_interp = interp_sonics123(df_aligned) #interpolating to the sensor's frequency                       
                # print('TRY, interpolate worked')
                # df_align_interp.to_csv(path_save+str(filename_only)+'_1.csv') #saving the new aligned, despiked, and interpolated df as a .csv file                       
                df_sonic2paros_interp = interp_sonics2paros(df_aligned)
                # df_sonic2paros_interp.to_csv(path_saveB+str(filename_only)+'_1.csv')
            else:
                df_align_interp = pd.DataFrame(np.nan, index=[0,1], columns=['base_index','Ur','Vr','Wr','T','u','v','w','alpha','beta'])
                df_sonic2paros_interp = pd.DataFrame(np.nan, index=range(0,1), columns=['base_index','Ur','Vr','Wr','T','u','v','w','alpha','beta'])
            df_align_interp.to_csv(path_save+str(filename_only)+'_1.csv') #saving the new aligned, despiked, and interpolated df as a .csv file                       
            df_sonic2paros_interp.to_csv(path_saveB+str(filename_only)+'_1.csv')
            print('Port 2 ran: '+filename)
            
        elif filename.startswith("mNode_Port3"):
            filename_only = filename[:-4]
            path_save = r"E:\ASIT-research\BB-ASIT\Level1_align-despike-interp\port3/"
            path_saveB = r'E:\ASIT-research\BB-ASIT\Level2_analysis\resample_sonic2paros/'
            s3_df = pd.read_csv(file, index_col=None, header = None) #read file into df
            s3_df.columns =['u', 'v', 'w', 'T', 'err_code','chk_sum'] #set column names to the variable          
            s3_df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
            if (len(s3_df)>=3000) & (s3_df['u'].isna().sum()<1000):                                    
                df_aligned = alignwind(s3_df) #perform align wind function
                # print('TRY, df_aligned worked')
                df_aligned['Ur'] = df_aligned['Ur'].apply(lambda x: np.nan if abs(x) > 31 else x) #despiking winds > 40kts
                df_aligned['Vr'] = df_aligned['Vr'].apply(lambda x: np.nan if abs(x) > 10 else x) #despiking v component
                df_aligned['Wr'] = df_aligned['Wr'].apply(lambda x: np.nan if abs(x) > 5 else x) #despiking w component
                # print('TRY, despike lines worked')
                df_align_interp = interp_sonics123(df_aligned) #interpolating to the sensor's frequency                       
                # print('TRY, interpolate worked')
                # df_align_interp.to_csv(path_save+str(filename_only)+'_1.csv') #saving the new aligned, despiked, and interpolated df as a .csv file                       
                df_sonic2paros_interp = interp_sonics2paros(df_aligned)
                # df_sonic2paros_interp.to_csv(path_saveB+str(filename_only)+'_1.csv')
            else:
                df_align_interp = pd.DataFrame(np.nan, index=[0,1], columns=['base_index','Ur','Vr','Wr','T','u','v','w','alpha','beta'])
                df_sonic2paros_interp = pd.DataFrame(np.nan, index=range(0,1), columns=['base_index','Ur','Vr','Wr','T','u','v','w','alpha','beta'])
            df_align_interp.to_csv(path_save+str(filename_only)+'_1.csv') #saving the new aligned, despiked, and interpolated df as a .csv file                       
            df_sonic2paros_interp.to_csv(path_saveB+str(filename_only)+'_1.csv')
            print('Port 3 ran: '+filename)
            
        elif filename.startswith("mNode_Port4"):
            filename_only = filename[:-4]
            path_save = r"E:\ASIT-research\BB-ASIT\Level1_align-despike-interp\port4/"
            path_saveB = r'E:\ASIT-research\BB-ASIT\Level2_analysis\resample_sonic2paros/'
            s4_df =pd.read_csv(file, index_col=None, header = None)
            s4_df.columns =['chk_1','chk_2','u', 'v', 'w', 'T', 'err_code']
            s4_df = s4_df[['u', 'v', 'w', 'T',]]
            s4_df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
            if (len(s4_df)>=3000) & (s4_df['u'].isna().sum()<1000):                                    
                df_aligned = alignwind(s4_df) #perform align wind function
                # print('TRY, df_aligned worked')
                df_aligned['Ur'] = df_aligned['Ur'].apply(lambda x: np.nan if abs(x) > 31 else x) #despiking winds > 40kts
                df_aligned['Vr'] = df_aligned['Vr'].apply(lambda x: np.nan if abs(x) > 10 else x) #despiking v component
                df_aligned['Wr'] = df_aligned['Wr'].apply(lambda x: np.nan if abs(x) > 5 else x) #despiking w component
                # print('TRY, despike lines worked')
                df_align_interp = interp_sonics4(df_aligned) #interpolating to the sensor's frequency                       
                # print('TRY, interpolate worked')
                # df_align_interp.to_csv(path_save+str(filename_only)+'_1.csv') #saving the new aligned, despiked, and interpolated df as a .csv file                       
                df_sonic2paros_interp = interp_sonics2paros(df_aligned)
                # df_sonic2paros_interp.to_csv(path_saveB+str(filename_only)+'_1.csv')                     
            else:
                df_align_interp = pd.DataFrame(np.nan, index=[0,1], columns=['base_index','Ur','Vr','Wr','T','u','v','w','alpha','beta'])
                df_sonic2paros_interp = pd.DataFrame(np.nan, index=range(0,1), columns=['base_index','Ur','Vr','Wr','T','u','v','w','alpha','beta'])
            df_align_interp.to_csv(path_save+str(filename_only)+'_1.csv') #saving the new aligned, despiked, and interpolated df as a .csv file                       
            df_sonic2paros_interp.to_csv(path_saveB+str(filename_only)+'_1.csv')
            print('Port 4 ran: '+filename)
        
        elif filename.startswith('mNode_Port5'):
            # Yday, Batt V, Tpan, Tair1, Tair2,  TIR, Pair, RH1, RH2, Solar, IR, IR ratio, Fix, GPS, Nsat
            # EX lines of data:
            # 106.4999,12.02,10.18,9.63,9.75,10.8,1053,75.83,75.53,323.1,-83.8,0.646,0,0,0
            # 106.4999,12.02,10.18,9.69,9.78,10.8,1053,75.83,75.26,323.1,-83.9,0.646,0,0,0
            filename_only = filename[:-4]
            path_save = r"E:\ASIT-research\BB-ASIT\Level1_align-despike-interp\port5/"
            s5_df = pd.read_csv(file, index_col=None, header = None)
            if (len(s5_df)>10)&(len(s5_df.columns)>=15):
            # if len(s5_df)==1200: #if the files have enough lined to match the frequency, go ahead and save as csv
                s5_df_met_interp = s5_df
                s5_df.columns =['yearDay', 'bat_volt', 'pannel_T', 'T1', 'T2','TIR',
                                'p_air', 'RH1', 'RH2', 'SW', 'IR', 'IR_ratio', 
                                'fix', 'GPS', 'Nsat']
                # s5_df.to_csv(path_save+str(filename_only)+'_1.csv')
            else:
                s5_df = pd.DataFrame(np.nan, index=range(0,1), columns=['yearDay', 'bat_volt', 'pannel_T', 'T1', 'T2','TIR',
                                'p_air', 'RH1', 'RH2', 'SW', 'IR', 'IR_ratio', 
                                'fix', 'GPS', 'Nsat'])
            s5_df.to_csv(path_save+str(filename_only)+'_1.csv')
            print('Port 5 ran: '+filename)
                
        elif filename.startswith('mNode_Port6'):
            filename_only = filename[:-4]
            path_save = r"E:\ASIT-research\BB-ASIT\Level1_align-despike-interp\port6/"
            s6_df = pd.read_csv(file,index_col=None, header = None) #read into a df
            s6_df.columns =['sensor','p'] #rename columns
            s6_df= s6_df[s6_df['sensor'] != 0] #get rid of any rows where the sensor is 0 because this is an error row
            s6_df_1 = s6_df[s6_df['sensor'] == 1] # make a df just for sensor 1
            s6_df_2 = s6_df[s6_df['sensor'] == 2] # make a df just for sensor 2
            s6_df_3 = s6_df[s6_df['sensor'] == 3] # make a df just for sensor 3
            
            if len(s6_df_1) >= 14400: #check that at least 75% of the 20 minutes was recorded for pressure 1
                df_paros_interp = interp_paros(s6_df_1) #interpolate to proper frequency
                s6_df_1_interp = df_paros_interp #rename                
                # print('IF worked')
            else: #if not enough points, make a df of NaNs that is the size of a properly interpolated df
                s6_df_1_interp = pd.DataFrame(np.nan, index=range(0,1), columns=['sensor','p'])
            s6_df_1_interp.to_csv(path_save+str(filename_only)+'L1_1.csv') #save as csv
            del df_paros_interp
                # print('except paros 1'+ filename)
                # try:
                #     df_paros_interp = interp_paros(s6_df_1)
                #     s6_df_1_interp = df_paros_interp
                #     s6_df_1_interp.to_csv(path_save+str(filename)+'_1.csv')
                #     del df_paros_interp
                # except:
                #     s6_df_1_interp = pd.DataFrame(np.nan, index=range(0,19200), columns=['sensor','p'])
                #     s6_df_1_interp.to_csv(path_save+str(filename)+'_1.csv')
                #     print('except paros 1')
                #     continue
            if len(s6_df_2) >= 14400: #check that at least 75% of the 20 minutes was recorded for pressure 1
                df_paros_interp = interp_paros(s6_df_2) #interpolate to proper frequency
                s6_df_2_interp = df_paros_interp #rename                
                # print('IF worked')
            else: #if not enough points, make a df of NaNs that is the size of a properly interpolated df
                s6_df_2_interp = pd.DataFrame(np.nan, index=range(0,1), columns=['sensor','p'])
            s6_df_2_interp.to_csv(path_save+str(filename_only)+'L2_1.csv') #save as csv
            del df_paros_interp
                # print('except paros 2'+ filename)
            # try:
            #     df_paros_interp = interp_paros(s6_df_2)
            #     s6_df_2_interp = df_paros_interp
            #     s6_df_2_interp.to_csv(path_save+str(filename)+'_1.csv')
            #     del df_paros_interp
            # except:
            #     s6_df_2_interp = pd.DataFrame(np.nan, index=range(0,19200), columns=['sensor','p'])
            #     s6_df_2_interp.to_csv(path_save+str(filename)+'_1.csv')
            #     print('except paros 2')
            #     continue
            if len(s6_df_3) >= 14400: #check that at least 75% of the 20 minutes was recorded for pressure 1
                df_paros_interp = interp_paros(s6_df_3) #interpolate to proper frequency
                s6_df_3_interp = df_paros_interp #rename                
                # print('IF worked')
            else: #if not enough points, make a df of NaNs that is the size of a properly interpolated df
                s6_df_3_interp = pd.DataFrame(np.nan, index=range(0,1), columns=['sensor','p'])
            s6_df_3_interp.to_csv(path_save+str(filename_only)+'L3_1.csv') #save as csv
            del df_paros_interp
                # print('except paros 3' + filename)
            # try:
            #     df_paros_interp = interp_paros(s6_df_3)
            #     s6_df_3_interp = df_paros_interp
            #     s6_df_3_interp.to_csv(path_save+str(filename)+'_1.csv')
            #     del df_paros_interp
            # except:
            #     s6_df_3_interp = pd.DataFrame(np.nan, index=range(0,19200), columns=['sensor','p'])
            #     s6_df_3_interp.to_csv(path_save+str(filename)+'_1.csv')
            #     print('except paros 3')
            #     continue
            # print('working')
            print('done with paros '+filename)


### come back to this and make the bad lines NaNs instead of deleting them
# then go back and check that this is done properly for the other ports as well.
        elif filename.startswith('mNode_Port7'):
            filename_only = filename[:-4]
            path_save = r"E:\ASIT-research\BB-ASIT\Level1_align-despike-interp\port7/"
            s7_df = pd.read_csv(file,index_col=None, header = None)
            s7_df.columns =['range','amplitude','quality']
            if s7_df['range'].isna().sum()<300: #make sure at least 75% of 20 minutes (at 1Hz frequency because of wave dropout) is recorded
                # s7_df = s7_df['all'].str.split(';', expand=True) #now separate into different columns
                # s7_df.columns =['range','amplitude','quality'] # name the columns
                # s7_df['range'] = s7_df['range'].str.lstrip('r') #get rid of leading 'r' in range column
                # s7_df['amplitude'] = s7_df['amplitude'].str.lstrip('a') #get rid of leading 'a' in amplitude column
                # s7_df['quality'] = s7_df['quality'].str.lstrip('q') #get rid of leading 'q' in quality column
                s7_df_interp = interp_lidar(s7_df) #interpolate to Lidar's sampling frequency
            else:
                s7_df_interp = pd.DataFrame(np.nan, index=range(0,1), columns=['range','amplitude','quality'])
            s7_df_interp.to_csv(path_save+str(filename_only)+'_1.csv') #save as csv
            print('Port 7 ran for file: '+ filename)
            print(len(s7_df_interp))
        
        else:
            print("file doesn't start with mNode_Port 1-7")
            continue


print('done')

