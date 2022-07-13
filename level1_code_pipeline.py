# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 09:11:31 2022

@author: oaklin

This is Level 1 pipeline: Taking the aligned, interpolated, despiked files from Level 0
and creating the variables (product terms) we will analyze in Level 2. Edited files are 
saved to the Level 2 folder, in their respective "port" sub-folder as .csv files. 


Input:
    .csv files per 20 min period per port from LEVEL_1 folder
Output:
    .csv files per 20 min period per port into LEVEL_2 folder
    
    
Variables created in this code:
Ports 1, 2, 3, 4:
    <u> = u_bar, 
    u' = u_p, 
    v' = v_p, 
    w' = w_p, 
    <T> = T_bar, 
    T' = T_p, 
    tke = tke, 
    u_horizontal = U_horiz, 
    u_streamwise = U_streamwise
    epsilon = epsilon
Port 5:
    IRt
Port 6:
    p'
Port 7:
    ??
    
"""

#%% Imports
#testing comment
import numpy as np
import pandas as pd
# from pandas import rolling_median
import os
# import matplotlib.pyplot as plt
import natsort
# import time
import math
# from scipy import interpolate
import scipy.signal as signal
# os.chdir(r'E:\mNode_test2folders\test')
print('done with imports')
#%%

filepath= r"E:\ASIT-research\BB-ASIT\Level1_align-despike-interp"
for root, dirnames, filenames in os.walk(filepath): #this is for looping through files that are in a folder inside another folder
    for filename in natsort.natsorted(filenames):
        file = os.path.join(root, filename)
        if filename.startswith("mNode_Port1"):
            filename_only = filename[:-6]
            path_save = r"E:\ASIT-research\BB-ASIT\Level2_analysis\port1/"
            path_saveEPSILON = r"E:\ASIT-research\BB-ASIT\Level2_analysis\epsilon_files"
            df_align_interp = pd.read_csv(file)            
            # print('read in file')
            if len(df_align_interp) > 2:                        
                u_prime = np.array(signal.detrend(df_align_interp['Ur']))
                v_prime = np.array(signal.detrend(df_align_interp['Vr']))
                w_prime = np.array(signal.detrend(df_align_interp['Wr']))
                T_prime = np.array(signal.detrend(df_align_interp['T']))
                # print('did detrend')
                U = np.array(df_align_interp['u'])
                V = np.array(df_align_interp['v'])
                W = np.array(df_align_interp['w'])
                T = np.array(df_align_interp['T'])
    
                c1 = 0.53
                fs = 32 #sampling frequency of sonics 1-3
                f, Pww = signal.welch(w_prime,fs,nperseg=1024) #pwelch function
                #converting to wavenumber spectrum
                k_arr = f/np.mean(U)*(2*math.pi)
                Pww_k_arr = Pww*np.mean(U)/(2*math.pi)
                epsilon_df = pd.DataFrame()
                epsilon_df['k']= k_arr
                epsilon_df['Pww_k']= Pww_k_arr
                epsilon_df.to_csv(path_saveEPSILON+str(filename_only)+'_epsilon.csv')
                # print('did this too')
                U_horiz = []
                U_streamwise = []
                # tke = []
                for i in range(len(df_align_interp)):
                    U_horizontal_i = math.sqrt((U[i]**2)+(V[i]**2))
                    U_horiz.append(U_horizontal_i)
                    U_streamwise_i = math.sqrt((U[i]**2)+(V[i]**2)+(W[i]**2))
                    U_streamwise.append(U_streamwise_i)
                    # wind_dir = math.atan3(v_orig_comp[i],u_orig_comp[i])
                    # tke_i = 0.5*((u_prime[i]**2)+(v_prime[i]**2)+(w_prime[i]**2))
                    # tke.append(tke_i)
                # print('did orig TKE')
                tke_avg = np.ones(len(df_align_interp))*(0.5*((np.mean(u_prime**2))+(np.mean(v_prime**2))+(np.mean(w_prime**2))))   
                # print('did average tke')
                # df_align_interp.assign(u_prime='u_p', v_prime='v_p', w_prime='w_p', 
                #                        T_prime='T_p', tke = 'tke', tke_avg='tke_avg', U_horiz = 'U_horiz',
                #                        U_streamwise = 'U_streamwise')
                df_align_interp['u_p']=u_prime
                df_align_interp['v_p']=v_prime
                df_align_interp['w_p']=w_prime
                df_align_interp['T_p']=T_prime
                df_align_interp['e_bar']=tke_avg
                df_align_interp['U_horiz']=U_horiz
                df_align_interp['U_streamwise']=U_streamwise
                # print('created new DF')
                df_align_interp.to_csv(path_save+str(filename_only)+'_2.csv')
            else:
                df_align_interp['u_p']=np.nan
                df_align_interp['v_p']=np.nan
                df_align_interp['w_p']=np.nan
                df_align_interp['T_p']=np.nan
                df_align_interp['e_bar']=np.nan
                df_align_interp['U_horiz']=np.nan
                df_align_interp['U_streamwise']=np.nan
                df_align_interp.to_csv(path_save+str(filename_only)+'_2.csv')
                df_align_interp.to_csv(path_save+str(filename_only)+'_2.csv')
            print('done with ' +filename)
            
        elif filename.startswith('mNode_Port2'):
            filename_only = filename[:-6]
            path_save = r"E:\ASIT-research\BB-ASIT\Level2_analysis\port2/"
            df_align_interp = pd.read_csv(file)
            # print('read in file')     
            if len(df_align_interp) > 2:                   
                u_prime = np.array(signal.detrend(df_align_interp['Ur']))
                v_prime = np.array(signal.detrend(df_align_interp['Vr']))
                w_prime = np.array(signal.detrend(df_align_interp['Wr']))
                T_prime = np.array(signal.detrend(df_align_interp['T']))
                # print('did detrend')
                U = np.array(df_align_interp['u'])
                V = np.array(df_align_interp['v'])
                W = np.array(df_align_interp['w'])
                T = np.array(df_align_interp['T'])
                fs = 32 #sampling frequency of sonics 1-3
                f, Pww = signal.welch(w_prime,fs,nperseg=1024) #pwelch function
                #converting to wavenumber spectrum
                k_arr = f/np.mean(U)*(2*math.pi)
                Pww_k_arr = Pww*np.mean(U)/(2*math.pi)
                epsilon_df = pd.DataFrame()
                epsilon_df['k']= k_arr
                epsilon_df['Pww_k']= Pww_k_arr
                epsilon_df.to_csv(path_saveEPSILON+str(filename_only)+'_epsilon.csv')
                # print('did this too')
                U_horiz = []
                U_streamwise = []
                # tke = []
                for i in range(len(df_align_interp)):
                    U_horizontal_i = math.sqrt((U[i]**2)+(V[i]**2))
                    U_horiz.append(U_horizontal_i)
                    U_streamwise_i = math.sqrt((U[i]**2)+(V[i]**2)+(W[i]**2))
                    U_streamwise.append(U_streamwise_i)
                    # wind_dir = math.atan3(v_orig_comp[i],u_orig_comp[i])
                    # tke_i = 0.5*((u_prime[i]**2)+(v_prime[i]**2)+(w_prime[i]**2))
                    # tke.append(tke_i)
                # print('did orig TKE')
                tke_avg = np.ones(len(df_align_interp))*(0.5*((np.mean(u_prime**2))+(np.mean(v_prime**2))+(np.mean(w_prime**2))))   
                # print('did average tke')
                # df_align_interp.assign(u_prime='u_p', v_prime='v_p', w_prime='w_p', 
                #                        T_prime='T_p', tke = 'tke', tke_avg='tke_avg', U_horiz = 'U_horiz',
                #                        U_streamwise = 'U_streamwise')
                df_align_interp['u_p']=u_prime
                df_align_interp['v_p']=v_prime
                df_align_interp['w_p']=w_prime
                df_align_interp['T_p']=T_prime
                df_align_interp['e_bar']=tke_avg
                df_align_interp['U_horiz']=U_horiz
                df_align_interp['U_streamwise']=U_streamwise
                # print('created new DF')
                df_align_interp.to_csv(path_save+str(filename_only)+'_2.csv')
            else:
                df_align_interp['u_p']=np.nan
                df_align_interp['v_p']=np.nan
                df_align_interp['w_p']=np.nan
                df_align_interp['T_p']=np.nan
                df_align_interp['e_bar']=np.nan
                df_align_interp['U_horiz']=np.nan
                df_align_interp['U_streamwise']=np.nan
                df_align_interp.to_csv(path_save+str(filename_only)+'_2.csv')
            print('done with ' +filename)
            
        elif filename.startswith('mNode_Port3'):
            filename_only = filename[:-6]
            path_save = r"E:\ASIT-research\BB-ASIT\Level2_analysis\port3/"
            df_align_interp = pd.read_csv(file)
            # print('read in file')            
            if len(df_align_interp) > 2:            
                u_prime = np.array(signal.detrend(df_align_interp['Ur']))
                v_prime = np.array(signal.detrend(df_align_interp['Vr']))
                w_prime = np.array(signal.detrend(df_align_interp['Wr']))
                T_prime = np.array(signal.detrend(df_align_interp['T']))
                # print('did detrend')
                U = np.array(df_align_interp['u'])
                V = np.array(df_align_interp['v'])
                W = np.array(df_align_interp['w'])
                T = np.array(df_align_interp['T'])
                fs = 32 #sampling frequency of sonics 1-3
                f, Pww = signal.welch(w_prime,fs,nperseg=1024) #pwelch function
                #converting to wavenumber spectrum
                k_arr = f/np.mean(U)*(2*math.pi)
                Pww_k_arr = Pww*np.mean(U)/(2*math.pi)
                epsilon_df = pd.DataFrame()
                epsilon_df['k']= k_arr
                epsilon_df['Pww_k']= Pww_k_arr
                epsilon_df.to_csv(path_saveEPSILON+str(filename_only)+'_epsilon.csv')
                # print('did this too')
                U_horiz = []
                U_streamwise = []
                # tke = []
                for i in range(len(df_align_interp)):
                    U_horizontal_i = math.sqrt((U[i]**2)+(V[i]**2))
                    U_horiz.append(U_horizontal_i)
                    U_streamwise_i = math.sqrt((U[i]**2)+(V[i]**2)+(W[i]**2))
                    U_streamwise.append(U_streamwise_i)
                    # wind_dir = math.atan3(v_orig_comp[i],u_orig_comp[i])
                    # tke_i = 0.5*((u_prime[i]**2)+(v_prime[i]**2)+(w_prime[i]**2))
                    # tke.append(tke_i)
                # print('did orig TKE')
                tke_avg = np.ones(len(df_align_interp))*(0.5*((np.mean(u_prime**2))+(np.mean(v_prime**2))+(np.mean(w_prime**2))))   
                # print('did average tke')
                # df_align_interp.assign(u_prime='u_p', v_prime='v_p', w_prime='w_p', 
                #                        T_prime='T_p', tke = 'tke', tke_avg='tke_avg', U_horiz = 'U_horiz',
                #                        U_streamwise = 'U_streamwise')
                df_align_interp['u_p']=u_prime
                df_align_interp['v_p']=v_prime
                df_align_interp['w_p']=w_prime
                df_align_interp['T_p']=T_prime
                df_align_interp['e_bar']=tke_avg
                df_align_interp['U_horiz']=U_horiz
                df_align_interp['U_streamwise']=U_streamwise
                # print('created new DF')
                df_align_interp.to_csv(path_save+str(filename_only)+'_2.csv')
            else:
                df_align_interp['u_p']=np.nan
                df_align_interp['v_p']=np.nan
                df_align_interp['w_p']=np.nan
                df_align_interp['T_p']=np.nan
                df_align_interp['e_bar']=np.nan
                df_align_interp['U_horiz']=np.nan
                df_align_interp['U_streamwise']=np.nan
                df_align_interp.to_csv(path_save+str(filename_only)+'_2.csv')
            print('done with ' +filename)
            
        elif filename.startswith("mNode_Port4"):
            filename_only = filename[:-6]
            path_save = r"E:\ASIT-research\BB-ASIT\Level2_analysis\port4/"
            df_align_interp = pd.read_csv(file)
            # print('read in file')      
            if len(df_align_interp) > 2:                  
                u_prime = np.array(signal.detrend(df_align_interp['Ur']))
                v_prime = np.array(signal.detrend(df_align_interp['Vr']))
                w_prime = np.array(signal.detrend(df_align_interp['Wr']))
                T_prime = np.array(signal.detrend(df_align_interp['T']))
                # print('did detrend')
                U = np.array(df_align_interp['u'])
                V = np.array(df_align_interp['v'])
                W = np.array(df_align_interp['w'])
                T = np.array(df_align_interp['T'])
                fs = 20 #sampling frequency of sonic 4
                f, Pww = signal.welch(w_prime,fs,nperseg=1024) #pwelch function
                #converting to wavenumber spectrum
                k_arr = f/np.mean(U)*(2*math.pi)
                Pww_k_arr = Pww*np.mean(U)/(2*math.pi)
                epsilon_df = pd.DataFrame()
                epsilon_df['k']= k_arr
                epsilon_df['Pww_k']= Pww_k_arr
                epsilon_df.to_csv(path_saveEPSILON+str(filename_only)+'_epsilon.csv')
                # print('did this too')
    
                U_horiz = []
                U_streamwise = []
                # tke = []
                for i in range(len(df_align_interp)):
                    U_horizontal_i = math.sqrt((U[i]**2)+(V[i]**2))
                    U_horiz.append(U_horizontal_i)
                    U_streamwise_i = math.sqrt((U[i]**2)+(V[i]**2)+(W[i]**2))
                    U_streamwise.append(U_streamwise_i)
                    # wind_dir = math.atan3(v_orig_comp[i],u_orig_comp[i])
                    # tke_i = 0.5*((u_prime[i]**2)+(v_prime[i]**2)+(w_prime[i]**2))
                    # tke.append(tke_i)
                # print('did orig TKE')
                tke_avg = np.ones(len(df_align_interp))*(0.5*((np.mean(u_prime**2))+(np.mean(v_prime**2))+(np.mean(w_prime**2))))   
                # print('did average tke')
                # df_align_interp.assign(u_prime='u_p', v_prime='v_p', w_prime='w_p', 
                #                        T_prime='T_p', tke = 'tke', tke_avg='tke_avg', U_horiz = 'U_horiz',
                #                        U_streamwise = 'U_streamwise')
                df_align_interp['u_p']=u_prime
                df_align_interp['v_p']=v_prime
                df_align_interp['w_p']=w_prime
                df_align_interp['T_p']=T_prime
                df_align_interp['e_bar']=tke_avg
                df_align_interp['U_horiz']=U_horiz
                df_align_interp['U_streamwise']=U_streamwise
                # print('created new DF')
                df_align_interp.to_csv(path_save+str(filename_only)+'_2.csv')
            else:
                df_align_interp['u_p']=np.nan
                df_align_interp['v_p']=np.nan
                df_align_interp['w_p']=np.nan
                df_align_interp['T_p']=np.nan
                df_align_interp['e_bar']=np.nan
                df_align_interp['U_horiz']=np.nan
                df_align_interp['U_streamwise']=np.nan
                df_align_interp.to_csv(path_save+str(filename_only)+'_2.csv')
            print('done with ' +filename)
            
        elif filename.startswith('mNode_Port5'):
            filename_only = filename[:-6]
            path_save = r"E:\ASIT-research\BB-ASIT\Level2_analysis\port5/"
            s5_df = pd.read_csv(file)
            sigma_sb = 5.67*(10**(-8))
            IRt = s5_df['IR'] + sigma_sb*(s5_df['TIR']+273.16)**4
            s5_df.assign(IRt = 'IRt')
            s5_df.to_csv(path_save+str(filename_only)+'_2.csv')
            print('done with ' +filename)
            
        elif filename.startswith('mNode_Port6'):
            filename_only = filename[:-6]
            path_save = r"E:\ASIT-research\BB-ASIT\Level2_analysis\port6/"
            if filename.endswith('L1_1.csv'):
                s6_df1 = pd.read_csv(file)
                p_prime_L1 = np.array(signal.detrend(s6_df1['p'])) #detrending produced the 'prime' term
                s6_df1.assign(p_prime_L1 = 'p_prime')
                s6_df1.to_csv(path_save+str(filename_only)+'L1_2.csv')                
            elif filename.endswith('L2_1.csv'):
                s6_df2 = pd.read_csv(file)
                p_prime_L2 = np.array(signal.detrend(s6_df2['p']))
                s6_df2.assign(p_prime_L2 = 'p_prime')
                s6_df2.to_csv(path_save+str(filename_only)+'L2_2.csv')
            elif filename.endswith('L3_1.csv'):
                s6_df3 = pd.read_csv(file)
                p_prime_L3 = np.array(signal.detrend(s6_df3['p']))
                s6_df3.assign(p_prime_L3 = 'p_prime')
                s6_df3.to_csv(path_save+str(filename_only)+'L3_2.csv')
            print('done with port 6')
        else:
            print("file doesn't start with mNode_Port 1-6")
            continue
        continue
# s1 = np.transpose(s1_align)
print('done')
# #%%
# bps = df_aligned.isnull().any(axis=1).sum()
# print(bps)
# #%%
# plt.plot(s1_u, label = "u")
# plt.plot(s1_v, label = "v")
# plt.plot(s1_w, label = "w")
# ax = plt.gca()
# ax.set_title("uvw_aligned_despike")
# plt.legend(loc='upper right')
# # ax.set_ylim([-12, 14])
# print('look for plot in "Plots" pane')