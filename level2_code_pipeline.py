# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 15:30:22 2022

@author: oaklin

This is Level 2 pipeline: Taking the variables made in Level 1 (and saved in 
.csv files) to analyze the terms of the TKE budget equation. 
Edited files are saved to the Level 3 folder, in their respective "TERM" sub-
folder as .csv files. 

Input:
    .csv files per 20 min period per port from LEVEL_2 folder
    .csv files ports 1-4 per 20 min period downsampled to paros freq. in LEVEL_2 
    resample_sonic2paros sub-folder
    <u>, u', v', w', <T>, T', tke', u_horizontal, u_streamwise
Output:
    .csv files per 20 min period per port

Variables created in this code:
Shear term:
    <u'w'>
    d<u>/dz
TKE term:
    <w'e'> ??? these will need to be in d/dz so not totally correct here
    d<w'e'>/dz
    1/rho
Buoyancy term:
    g/<T>    <T'w'>
Pressure work term:
    <w'p'> ??? these will need to be in d/dz so not totally correct here
    d<w'p'>/dz
    1/rho
Dissipation:
    epsilon
    
"""
#%%
import numpy as np
import pandas as pd
# from pandas import rolling_median
import os
import matplotlib.pyplot as plt
import natsort
import statistics
# import time
import math
import scipy.signal as signal
# os.chdir(r'E:\mNode_test2folders\test')
print('done with imports')
#%%
mean_df1 = pd.DataFrame()
mean_df2 = pd.DataFrame()
mean_df3 = pd.DataFrame()
mean_df4 = pd.DataFrame()

s1_UpWp_bar = []
s1_WpE_bar = []
s1_WpTp_bar = []

s2_UpWp_bar = []
s2_WpE_bar = []
s2_WpTp_bar = []

s3_UpWp_bar = []
s3_WpE_bar = []
s3_WpTp_bar = []

s4_UpWp_bar = []
s4_WpE_bar = []
s4_WpTp_bar = []

# s1_wind_dir_bar = []
# s1_U_horizontal_bar = []
# s1_u_prime_mean = []
# s1_v_prime_mean = []
# s1_w_prime_mean = []
# s1_T_prime_mean = []

path_saveA = r"E:\ASIT-research\BB-ASIT\Level3_mean\other/"
folderPath= r"E:\ASIT-research\BB-ASIT\Level2_analysis"
for root, dirnames,filenames in os.walk(folderPath): #this is for looping through files that are in a folder inside another folder
    for filename in natsort.natsorted(filenames):
        file = os.path.join(root, filename)
        if filename.startswith("mNode_Port1"):
        # file = os.path.join(root, filename)                
                df_sonic = pd.read_csv(filename)
                #variables from the dataframe: 
                    # <u> = u_bar, 
                    # u' = u_p, 
                    # v' = v_p, 
                    # w' = w_p, 
                    # <T> = T_bar, 
                    # T' = T_p, 
                    # tke = tke, 
                    # u_horizontal = U_horiz, 
                    # u_streamwise = U_streamwise
                
                UpWp_bar_i = np.nanmean(df_sonic["u_p"]*df_sonic["w_p"])
                s1_UpWp_bar.append(UpWp_bar_i)
                WpTp_bar_i = np.nanmean(df_sonic["w_p"]*df_sonic["T_p"])
                s1_WpTp_bar.append(WpTp_bar_i)
                WpE_bar_i = np.nanmean(df_sonic["w_p"]*df_sonic["tke"])
                s1_WpE_bar.append(WpE_bar_i)
                s1_u_bar=np.array(df_sonic["u_bar"].mean())
                s1_T_bar=np.array(df_sonic["T_bar"].mean())
                c1 = 0.53                
                goodk_df = df_sonic.loc[(df_sonic['k_arr']>1)&(df_sonic['k_arr']<5)]
                epsilon_goodk = (np.mean(goodk_df['Pww_k']*(goodk_df['k_arr']**(5/3)))/c1)**(3/2)
                epsilon_allk = (np.mean(df_sonic['Pww_k']*(df_sonic['k_arr']**(5/3)))/c1)**(3/2)
                mean_df1.assign(s1_UpWp_bar = '<UpWp>',s1_WpTp_bar = '<WpTp>',s1_WpE_bar = '<WpE>',s1_u_bar = '<u>',s1_T_bar = '<T>',epsilon_goodk = 'epsilon_goodk',epsilon_allk = 'epsilon_allk')    
        
        elif filename.startswith("mNode_Port2"):
                df_sonic = pd.read_csv(filename)
                #variables from the dataframe: 
                    # <u> = u_bar, 
                    # u' = u_p, 
                    # v' = v_p, 
                    # w' = w_p, 
                    # <T> = T_bar, 
                    # T' = T_p, 
                    # tke = tke, 
                    # u_horizontal = U_horiz, 
                    # u_streamwise = U_streamwise
                
                UpWp_bar_i = np.nanmean(df_sonic["u_p"]*df_sonic["w_p"])
                s2_UpWp_bar.append(UpWp_bar_i)
                WpTp_bar_i = np.nanmean(df_sonic["w_p"]*df_sonic["T_p"])
                s2_WpTp_bar.append(WpTp_bar_i)
                WpE_bar_i = np.nanmean(df_sonic["w_p"]*df_sonic["tke"])
                s2_WpE_bar.append(WpE_bar_i)
                s2_u_bar=np.array(df_sonic["u_bar"].mean())
                s2_T_bar=np.array(df_sonic["T_bar"].mean())            
                c1 = 0.53                
                goodk_df = df_sonic.loc[(df_sonic['k_arr']>1)&(df_sonic['k_arr']<5)]
                epsilon_goodk = (np.mean(goodk_df['Pww_k']*(goodk_df['k_arr']**(5/3)))/c1)**(3/2)
                epsilon_allk = (np.mean(df_sonic['Pww_k']*(df_sonic['k_arr']**(5/3)))/c1)**(3/2)
                mean_df2.assign(s2_UpWp_bar = '<UpWp>',s2_WpTp_bar = '<WpTp>',s2_WpE_bar = '<WpE>',s2_u_bar = '<u>',s2_T_bar = '<T>',epsilon_goodk = 'epsilon_goodk',epsilon_allk = 'epsilon_allk')                
                
        elif filename.startswith("mNode_Port3"):
                df_sonic = pd.read_csv(filename)
                #variables from the dataframe: 
                    # <u> = u_bar, 
                    # u' = u_p, 
                    # v' = v_p, 
                    # w' = w_p, 
                    # <T> = T_bar, 
                    # T' = T_p, 
                    # tke = tke, 
                    # u_horizontal = U_horiz, 
                    # u_streamwise = U_streamwise
                
                UpWp_bar_i = np.nanmean(df_sonic["u_p"]*df_sonic["w_p"])
                s3_UpWp_bar.append(UpWp_bar_i)
                WpTp_bar_i = np.nanmean(df_sonic["w_p"]*df_sonic["T_p"])
                s3_WpTp_bar.append(WpTp_bar_i)
                WpE_bar_i = np.nanmean(df_sonic["w_p"]*df_sonic["tke"])
                s3_WpE_bar.append(WpE_bar_i)
                s3_u_bar=np.array(df_sonic["u_bar"].mean())
                s3_T_bar=np.array(df_sonic["T_bar"].mean())
                c1 = 0.53                
                goodk_df = df_sonic.loc[(df_sonic['k_arr']>1)&(df_sonic['k_arr']<5)]
                epsilon_goodk = (np.mean(goodk_df['Pww_k']*(goodk_df['k_arr']**(5/3)))/c1)**(3/2)
                epsilon_allk = (np.mean(df_sonic['Pww_k']*(df_sonic['k_arr']**(5/3)))/c1)**(3/2)
                mean_df3.assign(s3_UpWp_bar = '<UpWp>',s3_WpTp_bar = '<WpTp>',s3_WpE_bar = '<WpE>',s3_u_bar = '<u>',s3_T_bar = '<T>',epsilon_goodk = 'epsilon_goodk',epsilon_allk = 'epsilon_allk')                
                
        elif filename.startswith("mNode_Port4"):
                df_sonic = pd.read_csv(filename)
                #variables from the dataframe: 
                    # <u> = u_bar, 
                    # u' = u_p, 
                    # v' = v_p, 
                    # w' = w_p, 
                    # <T> = T_bar, 
                    # T' = T_p, 
                    # tke = tke, 
                    # u_horizontal = U_horiz, 
                    # u_streamwise = U_streamwise
                
                UpWp_bar_i = np.nanmean(df_sonic["u_p"]*df_sonic["w_p"])
                s4_UpWp_bar.append(UpWp_bar_i)
                WpTp_bar_i = np.nanmean(df_sonic["w_p"]*df_sonic["T_p"])
                s4_WpTp_bar.append(WpTp_bar_i)
                WpE_bar_i = np.nanmean(df_sonic["w_p"]*df_sonic["tke"])
                s4_WpE_bar.append(WpE_bar_i)
                s4_u_bar=np.array(df_sonic["u_bar"].mean())
                s4_T_bar=np.array(df_sonic["T_bar"].mean())
                c1 = 0.53                
                goodk_df = df_sonic.loc[(df_sonic['k_arr']>1)&(df_sonic['k_arr']<5)]
                epsilon_goodk = (np.mean(goodk_df['Pww_k']*(goodk_df['k_arr']**(5/3)))/c1)**(3/2)
                epsilon_allk = (np.mean(df_sonic['Pww_k']*(df_sonic['k_arr']**(5/3)))/c1)**(3/2)
                mean_df4.assign(s4_UpWp_bar = '<UpWp>',s4_WpTp_bar = '<WpTp>',s4_WpE_bar = '<WpE>',s4_u_bar = '<u>',s4_T_bar = '<T>',epsilon_goodk = 'epsilon_goodk',epsilon_allk = 'epsilon_allk')                
                
        else:
            print('not ports 1-4')
            continue
    mean_df1.to_csv(path_saveA+'sonic1'+'_meanComponents.csv')
    mean_df2.to_csv(path_saveA+'sonic2'+'_meanComponents.csv')
    mean_df3.to_csv(path_saveA+'sonic3'+'_meanComponents.csv')
    mean_df4.to_csv(path_saveA+'sonic4'+'_meanComponents.csv')
        
        
s1_WpPp = []
s2_WpPp = []
s3_WpPp = []
s4_WpPp = []

path_saveB = r"E:\ASIT-research\BB-ASIT\Level3_mean\pressure/"
folderPath_pressure= r"E:\ASIT-research\BB-ASIT\Level2_analysis"
for root, dirnames,filenames in os.walk(folderPath_pressure): #this is for looping through files that are in a folder inside another folder
    for filename in natsort.natsorted(filenames):
        file = os.path.join(root, filename)
        if filename.startswith("mNode_Port1"):
            df_sonic1 = pd.read_csv(filename)
            Wp_1 = np.array(df_sonic1['w_p'])
        elif filename.startswith("mNode_Port2"):
            df_sonic2 = pd.read_csv(filename)
            Wp_2 = np.array(df_sonic2['w_p'])
        elif filename.startswith("mNode_Port3"):
            df_sonic3 = pd.read_csv(filename)
            Wp_3 = np.array(df_sonic3['w_p'])
        elif filename.startswith("mNode_Port4"):
            df_sonic4 = pd.read_csv(filename)
            Wp_4 = np.array(df_sonic4['w_p'])
        elif filename.endswith("L1_2.csv"):
            df_paros1 = pd.read_csv(filename)
            Pp_1 = np.array(df_paros1['p_prime'])
        elif filename.endswith("L2_2.csv"):
            df_paros2 = pd.read_csv(filename)
            Pp_2 = np.array(df_paros2['p_prime'])
        elif filename.endswith("L3_2.csv"):
            df_paros3 = pd.read_csv(filename)
            Pp_3 = np.array(df_paros3['p_prime'])
        else:
            continue
        for i in range(len(df_paros1)):
            s1_WpPp_i = Wp_1[i]*Pp_1[i]
            s1_WpPp.append(s1_WpPp_i)
            s2_WpPp_i = Wp_2[i]*Pp_2[i]
            s2_WpPp.append(s2_WpPp_i)
            s3_WpPp_i = Wp_3[i]*Pp_3[i]
            s3_WpPp.append(s3_WpPp_i)
            s4_WpPp_i = Wp_4[i]*Pp_3[i]
            s4_WpPp.append(s4_WpPp_i)
        s1_WpPp_bar = np.nanmean(s1_WpPp)
        s2_WpPp_bar = np.nanmean(s2_WpPp)
        s3_WpPp_bar = np.nanmean(s3_WpPp)
        s4_WpPp_bar = np.nanmean(s4_WpPp)
        # df_meanWpPp1 = pd.DataFrame()
        # df_meanWpPp1.assign(s1_WpPp_bar='<WpPp>')
        mean_df1.assign(s1_WpPp_bar='<WpPp>')
        # df_meanWpPp1.to_csv(path_saveB+filename+'_meanComponent_WpPp.csv')
        # df_meanWpPp2 = pd.DataFrame()
        # df_meanWpPp2.assign(s2_WpPp_bar='<WpPp>')
        mean_df2.assign(s2_WpPp_bar='<WpPp>')
        # df_meanWpPp2.to_csv(path_saveB+filename+'_meanComponent_WpPp.csv')
        # df_meanWpPp3 = pd.DataFrame()
        # df_meanWpPp3.assign(s3_WpPp_bar='<WpPp>')
        mean_df3.assign(s3_WpPp_bar='<WpPp>')
        # df_meanWpPp3.to_csv(path_saveB+filename+'_meanComponent_WpPp.csv')
        # df_meanWpPp4 = pd.DataFrame()
        # df_meanWpPp4.assign(s4_WpPp_bar='<WpPp>')
        mean_df4.assign(s4_WpPp_bar='<WpPp>')
        # df_meanWpPp4.to_csv(path_saveB+filename+'_meanComponent_WpPp.csv')
    mean_df1.to_csv(path_saveB+'sonic1'+'_meanComponents.csv')
    mean_df2.to_csv(path_saveB+'sonic2'+'_meanComponents.csv')
    mean_df3.to_csv(path_saveB+'sonic3'+'_meanComponents.csv')
    mean_df4.to_csv(path_saveB+'sonic4'+'_meanComponents.csv')
print('all done with this section of getting the MEANs in the code')

print('Now onto new section for doing d()/dz of variables')
dz12 = 2.695
dz23 = 1.54
dz34 = 3.67
Du_barDz_12 = []
DWpPp_barDz_12 = []
DWpE_barDz_12 = []

Du_barDz_23 = []
DWpPp_barDz_23 = []
DWpE_barDz_23 = []

Du_barDz_34 = []
DWpPp_barDz_34 = []
DWpE_barDz_34 = []
# need to take the average from <WpPp> per height as well as the average of <u>
# for consecutive sonic levels for each file
#will loop through

path_saveC = r"E:\ASIT-research\BB-ASIT\Level3_mean\dz_terms/"
u_bar1 = np.array(mean_df1['<u>'])
u_bar2 = np.array(mean_df2['<u>'])
u_bar3 = np.array(mean_df3['<u>'])
u_bar4 = np.array(mean_df4['<u>'])
WpPp_bar1 = np.array(mean_df1['<WpPp>'])
WpPp_bar2 = np.array(mean_df2['<WpPp>'])
WpPp_bar3 = np.array(mean_df3['<WpPp>'])
WpPp_bar4 = np.array(mean_df4['<WpPp>'])
WpE_bar1 = np.array(mean_df1['<WpE>'])
WpE_bar2 = np.array(mean_df2['<WpE>'])
WpE_bar3 = np.array(mean_df3['<WpE>'])
WpE_bar4 = np.array(mean_df4['<WpE>'])

for i in range(len(mean_df1)-1):    
    Du_barDz_12_i = (u_bar2[i]-u_bar1[i])/dz12
    Du_barDz_12.append(Du_barDz_12_i)
    Du_barDz_23_i = (u_bar3[i]-u_bar2[i])/dz23
    Du_barDz_23.append(Du_barDz_23_i)
    Du_barDz_34_i = (u_bar4[i]-u_bar3[i])/dz34
    Du_barDz_34.append(Du_barDz_34_i)
    
    DWpPp_barDz_12_i = (WpPp_bar2[i]-WpPp_bar1[i])/dz12
    DWpPp_barDz_12.append(DWpPp_barDz_12_i)
    DWpPp_barDz_23_i = (WpPp_bar3[i]-WpPp_bar2[i])/dz23
    DWpPp_barDz_23.append(DWpPp_barDz_23_i)
    DWpPp_barDz_34_i = (WpPp_bar4[i]-WpPp_bar3[i])/dz34
    DWpPp_barDz_34.append(DWpPp_barDz_34_i)
    
    DWpE_barDz_12_i = (WpE_bar2[i]-WpE_bar1[i])/dz12
    DWpE_barDz_12.append(DWpE_barDz_12_i)
    DWpE_barDz_23_i = (WpE_bar3[i]-WpE_bar2[i])/dz23
    DWpE_barDz_23.append(DWpE_barDz_23_i)
    DWpE_barDz_34_i = (WpE_bar4[i]-WpE_bar3[i])/dz34
    DWpE_barDz_34.append(DWpE_barDz_34_i)

dz12_df = pd.DataFrame()
dz23_df = pd.DataFrame()
dz34_df = pd.DataFrame()
dz12_df.assign(Du_barDz_12 = '<dU/dz>',DWpPp_barDz_12 = '<dWpPp/dz>',DWpE_barDz_12= '<dWpE/dz>' )
dz23_df.assign(Du_barDz_23 = '<dU/dz>',DWpPp_barDz_23 = '<dWpPp/dz>',DWpE_barDz_23= '<dWpE/dz>' )
dz34_df.assign(Du_barDz_34 = '<dU/dz>',DWpPp_barDz_34 = '<dWpPp/dz>',DWpE_barDz_34= '<dWpE/dz>' )
dz12_df.to_csv(path_saveC+"dzTerms_L12.csv")
dz23_df.to_csv(path_saveC+"dzTerms_L23.csv")
dz34_df.to_csv(path_saveC+"dzTerms_L34.csv")
print('all done with this section of getting the d/dz terms in the code')

print('Now onto new section for averaging sonics at 4 places to be "in 3" to align with d/dz zones')
g = 9.81
DUpWp_barDz_12 = []
DUpWp_barDz_23 = []
DUpWp_barDz_34 = []
DWpTp_barDz_12 = []
DWpTp_barDz_23 = []
DWpTp_barDz_34 = []
# DT_barDz_12 = []
# DT_barDz_23 = []
# DT_barDz_34 = []
T_bar1 = np.array(mean_df1['<T>'])
T_bar2 = np.array(mean_df2['<T>'])
T_bar3 = np.array(mean_df3['<T>'])
T_bar4 = np.array(mean_df4['<T>'])
UpWp_bar1 = np.array(mean_df1['<UpWp>'])
UpWp_bar2 = np.array(mean_df2['<UpWp>'])
UpWp_bar3 = np.array(mean_df3['<UpWp>'])
UpWp_bar4 = np.array(mean_df4['<UpWp>'])
WpTp_bar1 = np.array(mean_df1['<WpTp>'])
WpTp_bar2 = np.array(mean_df2['<WpTp>'])
WpTp_bar3 = np.array(mean_df3['<WpTp>'])
WpTp_bar4 = np.array(mean_df4['<WpTp>'])

for i in range(len(mean_df1)-1):
    # DT_barDz_12_i = (T_bar2[i]-T_bar1[i])/2
    # DT_barDz_12.append(DT_barDz_12_i)
    # DT_barDz_23_i = (T_bar3[i]-T_bar2[i])/2
    # DT_barDz_23.append(DT_barDz_23_i)
    # DT_barDz_34_i = (T_bar4[i]-T_bar3[i])/2
    # DT_barDz_34.append(DT_barDz_34_i)
    
    DUpWp_barDz_12_i = (UpWp_bar2[i]-UpWp_bar1[i])/2
    DUpWp_barDz_12.append(DUpWp_barDz_12_i)
    DUpWp_barDz_23_i = (UpWp_bar3[i]-UpWp_bar2[i])/2
    DUpWp_barDz_23.append(DUpWp_barDz_23_i)
    DUpWp_barDz_34_i = (UpWp_bar4[i]-UpWp_bar3[i])/2
    DUpWp_barDz_34.append(DUpWp_barDz_34_i)
    
    DWpTp_barDz_12_i = ((g/T_bar2[i]*WpTp_bar2[i])-(g/T_bar1[i]*WpTp_bar1[i]))/2
    DWpTp_barDz_12.append(DWpTp_barDz_12_i)
    DWpTp_barDz_23_i = ((g/T_bar3[i]*WpTp_bar3[i])-(g/T_bar2[i]*WpTp_bar2[i]))/2
    DWpTp_barDz_23.append(DWpTp_barDz_23_i)
    DWpTp_barDz_34_i = ((g/T_bar4[i]*WpTp_bar4[i])-(g/T_bar3[i]*WpTp_bar3[i]))/2
    DWpTp_barDz_34.append(DWpTp_barDz_34_i)
dz12_df.assign(DWpTp_barDz_12 = 'g<TpWp>/<T>',DUpWp_barDz_12 = '<UpWp>')
dz23_df.assign(DWpTp_barDz_23 = 'g<TpWp>/<T>',DUpWp_barDz_23 = '<UpWp>')
dz34_df.assign(DWpTp_barDz_34 = 'g<TpWp>/<T>',DUpWp_barDz_34 = '<UpWp>')             