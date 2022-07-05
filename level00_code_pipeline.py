# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 09:40:48 2022

@author: oaklin keefe

This is Level 0 pipeline: taking raw .dat files and turning them into a .csv file                                                                                          

Input:
    .dat files per 20 min period per port from *raw_CAN_edit folder
Output:
    .csv files per 20 min period per port into LEVEL_1 folder
    
"""
#%%
import numpy as np
import pandas as pd
import os
import natsort
import re

print('done with imports')

#%%
filepath= r"E:\mNode_test2folders\mN220509"
for root, dirnames, filenames in os.walk(filepath): #this is for looping through files that are in a folder inside another folder
    for filename in natsort.natsorted(filenames):
        file = os.path.join(root, filename)
        filename_only = filename[:-4]
        if filename.startswith("mNode_Port1"):
            path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port1/"
            regex = r"\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{2}(.{1}\d{1}\D{1}\d{2})\s{4}(\d{1}\D{1}\d{2})\s{1}(\S{2})\s{1,3}(\S{1,2})"
            textfile = open(file, 'r')
            matches = []
            # reg = re.compile(regex)
            for line in textfile:
                matches.append(re.match(regex,line))
            textfile.close()
            newFileName = str(filename_only)+".txt"
            lines = []
            with open(os.path.join(path_save,newFileName), "w") as myFile:
                for match in matches:
                    if match is None:
                        print(r"Nan,Nan,NaN,NaN,NaN,NaN", file=myFile)
                    else:
                        new_line = ','.join(match.groups())
                        print(new_line, file=myFile)
        elif filename.startswith("mNode_Port2"):
            path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port2/"
            regex = r"\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{2}(.{1}\d{1}\D{1}\d{2})\s{4}(\d{1}\D{1}\d{2})\s{1}(\S{2})\s{1,3}(\S{1,2})"
            textfile = open(file, 'r')
            matches = []
            # reg = re.compile(regex)
            for line in textfile:
                matches.append(re.match(regex,line))
            textfile.close()
            newFileName = str(filename_only)+".txt"
            lines = []
            with open(os.path.join(path_save,newFileName), "w") as myFile:
                for match in matches:
                    if match is None:
                        print(r"Nan,Nan,NaN,NaN,NaN,NaN", file=myFile)
                    else:
                        new_line = ','.join(match.groups())
                        print(new_line, file=myFile)
        elif filename.startswith("mNode_Port3"):
            path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port3/"
            regex = r"\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{2}(.{1}\d{1}\D{1}\d{2})\s{4}(\d{1}\D{1}\d{2})\s{1}(\S{2})\s{1,3}(\S{1,2})"
            textfile = open(file, 'r')
            matches = []
            # reg = re.compile(regex)
            for line in textfile:
                matches.append(re.match(regex,line))
            textfile.close()
            newFileName = str(filename_only)+".txt"
            lines = []
            with open(os.path.join(path_save,newFileName), "w") as myFile:
                for match in matches:
                    if match is None:
                        print(r"Nan,Nan,NaN,NaN,NaN,NaN", file=myFile)
                    else:
                        new_line = ','.join(match.groups())
                        print(new_line, file=myFile)
        elif filename.startswith("mNode_Port4"):
            path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port4/"
            regex = r".{4}\d{2}.{2}\d{1,2}.{1}\d{2}.{2}\d{1,2}.{1}\d{2}.{2}\d{1,2}.{1}\d{2}.{2}\d{1,2}.{1}\d{2}.{4}"
            textfile = open(file, 'r')
            matches = []
            # reg = re.compile(regex)
            for line in textfile:
                matches.append(re.match(regex,line))
            textfile.close()
            newFileName = str(filename_only)+".txt"
            lines = []
            with open(os.path.join(path_save,newFileName), "w") as myFile:
                for match in matches:
                    if match is None:
                        print(r"Nan,Nan,NaN,NaN,NaN,NaN,NaN", file=myFile)
                    else:
                        new_line = ','.join(match.groups())
                        print(new_line, file=myFile)
#%%
# Testing below
# filename = r"E:\mNode_test2folders\mN220509\mNode_Port4_20220509_100000.dat"
# path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port1/"
# regex = r".{4}\d{2}.{2}\d{1,2}.{1}\d{2}.{2}\d{1,2}.{1}\d{2}.{2}\d{1,2}.{1}\d{2}.{2}\d{1,2}.{1}\d{2}.{4}"
# # filename = r"E:\mNode_test2folders\mN220509\mNode_Port1_20220509_002000.dat"    

# textfile = open(filename, 'r')
# matches = []
# reg = re.compile(regex)
# for line in textfile:
#     matches.append(re.match(regex,line))
# textfile.close()
# #%%

# save_path = r'E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port1'

# newFileName = "mNode_Port1_20220509_004000.txt"

# import os.path
# lines = []
# with open(os.path.join(save_path,newFileName), "w") as myFile:
#     for match in matches:
#         if match is None:
#             print(r"Nan,Nan,NaN,NaN,NaN,NaN", file=myFile)
#         else:
#             new_line = ','.join(match.groups())
#             print(new_line, file=myFile)

# # lines = []
# # with open(filename+".txt",'w') as myFile:
# #     for match in matches:
# #         if match is None:
# #             print(r"Nan,Nan,NaN,NaN,NaN,NaN", file=myFile)
# #         else:
# #             new_line = ','.join(match.groups())
# #             print(new_line, file=myFile)

# # df = pd.read_csv(myFile)
# # matches_df.to_csv(path_save+'mNode_Port1_20220509_002000.csv')
# print('done')