# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 09:40:48 2022

@author: oaklin keefe

This is Level 00 pipeline: taking raw .dat files and turning them into a .txt file                                                                                          
First we read in the files and make sure there are enough input lines to process, and if so
then we run reg-exs to make sure the lines don't have any errors, before we save as a text file
with commas separating the columns so that we can later read it in as a .csv file without any
trouble.
Input:
    .dat files per 20 min period per port from *raw_CAN_edit folder
Output:
    .txt files per 20 min period per port into r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved" 
    plus sub-folder
    
"""
#%%
import numpy as np
import pandas as pd
import os
import natsort
import re

print('done with imports')

#%%
filepath= r"E:\ASIT-research\BB-ASIT\Level0_RAW"
for root, dirnames, filenames in os.walk(filepath): #this is for looping through files that are in a folder inside another folder
    for filename in natsort.natsorted(filenames):
        file = os.path.join(root, filename)
        filename_only = filename[:-4]
        # if filename.startswith("mNode_Port1"):
        #     if (os.path.getsize(file) >= 1420500): #1388 kb ~1420850
        #         path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port1/"
        #         # regex = r"\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{2}(.{1}\d{1}\D{1}\d{2})\s{4}(\d{1}\D{1}\d{2})\s{1}(\S{2})\s{1,3}(\S{1,2})"
        #         regex = r"\s{2,}([-]?\d*[.]?\d*)\s{1,}([-]?\d*[.]?\d*)\s{2,}([-]?\d*[.]?\d*)\s{1,}([-]?\d*[.]?\d*)\s{1}(\S{2,})\s{1,}(\S{1,})"
        #         textfile = open(file, 'r')
        #         matches = []
        #         # reg = re.compile(regex)
        #         for line in textfile:
        #             matches.append(re.match(regex,line))
        #         textfile.close()
        #         newFileName = str(filename_only)+".txt"
        #         lines = []
        #         with open(os.path.join(path_save,newFileName), "w") as myFile:
        #             for match in matches:
        #                 if match is None:
        #                     print(r"Nan,Nan,NaN,NaN,NaN,NaN", file=myFile)
        #                 else:
        #                     new_line = ','.join(match.groups())
        #                     print(new_line, file=myFile)
        #                     ###this took 13 mins
        if filename.startswith("mNode_Port2"):
            if (os.path.getsize(file) >= 1420500): #1388 kb ~1420850
                path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port2/"
                # regex = r"\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{2}(.{1}\d{1}\D{1}\d{2})\s{4}(\d{1}\D{1}\d{2})\s{1}(\S{2})\s{1,3}(\S{1,2})"
                regex = r"\s{2,}([-]?\d*[.]?\d*)\s{1,}([-]?\d*[.]?\d*)\s{1,}([-]?\d*[.]?\d*)\s{1,}([-]?\d*[.]?\d*)\s{1}(\S{2,})\s{1,}(\S{1,})"
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
                            ###this took 13 minutes
        # elif filename.startswith("mNode_Port3"):
        #     if (os.path.getsize(file) >= 1420500): #1388 kb ~1420850
        #         path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port3/"
        #         # regex = r"\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{1,2}(.{1}\d{1,2}\D{1}\d{2})\s{2}(.{1}\d{1}\D{1}\d{2})\s{4}(\d{1}\D{1}\d{2})\s{1}(\S{2})\s{1,3}(\S{1,2})"
        #         regex = r"\s{2,}([-]?\d*[.]?\d*)\s{1,}([-]?\d*[.]?\d*)\s{2,}([-]?\d*[.]?\d*)\s{1,}([-]?\d*[.]?\d*)\s{1}(\S{2,})\s{1,}(\S{1,})"
        #         textfile = open(file, 'r')
        #         matches = []
        #         # reg = re.compile(regex)
        #         for line in textfile:
        #             matches.append(re.match(regex,line))
        #         textfile.close()
        #         newFileName = str(filename_only)+".txt"
        #         lines = []
        #         with open(os.path.join(path_save,newFileName), "w") as myFile:
        #             for match in matches:
        #                 if match is None:
        #                     print(r"Nan,Nan,NaN,NaN,NaN,NaN", file=myFile)
        #                 else:
        #                     new_line = ','.join(match.groups())
        #                     print(new_line, file=myFile)
        # elif filename.startswith("mNode_Port4"):
        #     if (os.path.getsize(file) >= 958950): #679 kb ~958961
        #         path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port4/"
        #         # regex = r"(.{3}).{1}(\d{2}).{1}(.{1}\d{1,2}.{1}\d{2}).{1}(.{1}\d{1,2}.{1}\d{2}).{1}(.{1}\d{1,2}.{1}\d{2}).{1}(.{1}\d{1,2}.{1}\d{2}).{1}(.{3})"
        #         regex = r"\D{1}(\d*)[,]{1}([-+]?\d*[.]?\d*)[,]{1}([-+]?\d*[.]?\d*)[,]{1}([-+]?\d*[.]?\d*)[,]{1}([-+]?\d*[.]?\d*)[,]{1}([-+]?\d*[.]?\d*)[,]{1}\D{1}([[:alnum:]]*)"
        #         textfile = open(file, 'r')
        #         matches = []
        #         # reg = re.compile(regex)
        #         for line in textfile:
        #             matches.append(re.match(regex,line))
        #         textfile.close()
        #         newFileName = str(filename_only)+".txt"
        #         lines = []
        #         with open(os.path.join(path_save,newFileName), "w") as myFile:
        #             for match in matches:
        #                 if match is None:
        #                     print(r"Nan,Nan,NaN,NaN,NaN,NaN,NaN", file=myFile)
        #                 else:
        #                     new_line = ','.join(match.groups())
        #                     print(new_line, file=myFile)
        # elif filename.startswith("mNode_Port5"):
        #     if (os.path.getsize(file) >= 83000): #82 kb ~83374
        #         path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port5/"
        #         regex = r"(\d*[.]?\d*)[,]{1}(\d*[.]?\d*)[,]{1}(\d*[.]?\d*)[,]{1}(\d*[.]?\d*)[,]{1}(\d*[.]?\d*)[,]{1}(\d*[.]?\d*)[,]{1}(\d{3,4})[,]{1}(\d*[.]?\d*)[,]{1}(\d*[.]?\d*)[,]{1}([-]?\d*[.]?\d*)[,]{1}([-]?\d*[.]?\d*)[,]{1}([-]?\d*[.]?\d*)[,]{1}([-]?\d*[.]?\d*)[,]{1}([-]?\d*[.]?\d*)[,]{1}([-]?\d*[.]?\d*)"
        #         textfile = open(file, 'r')
        #         matches = []
        #         # reg = re.compile(regex)
        #         for line in textfile:
        #             matches.append(re.match(regex,line))
        #         textfile.close()
        #         newFileName = str(filename_only)+".txt"
        #         lines = []
        #         with open(os.path.join(path_save,newFileName), "w") as myFile:
        #             for match in matches:
        #                 if match is None:
        #                     print(r"Nan,Nan,NaN,NaN,NaN,NaN,NaN,Nan,Nan,NaN,NaN,NaN,NaN,NaN,NaN", file=myFile)
        #                 else:
        #                     new_line = ','.join(match.groups())
        #                     print(new_line, file=myFile)
                        
        # elif filename.startswith("mNode_Port6"):
        #     if (os.path.getsize(file) >= 1030000): #1013 kb ~1036761
        #         path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port6/"
        #         regex = r".{4}(\d{1})(\d{3,4}.{1}\d{1,})"
        #         textfile = open(file, 'r')
        #         matches = []
        #         # reg = re.compile(regex)
        #         for line in textfile:
        #             matches.append(re.match(regex,line))
        #         textfile.close()
        #         newFileName = str(filename_only)+".txt"
        #         lines = []
        #         with open(os.path.join(path_save,newFileName), "w") as myFile:
        #             for match in matches:
        #                 if match is None:
        #                     print(r"Nan,Nan", file=myFile)
        #                 else:
        #                     new_line = ','.join(match.groups())
        #                     print(new_line, file=myFile)
                        
        # elif filename.startswith("mNode_Port7"):
        #     if (os.path.getsize(file) >= 240000): #241 kb ~246116
        #         path_save = r"E:\ASIT-research\BB-ASIT\Level1_errorLinesRemoved\Port7/"
        #         regex = r"[r](\d{1}.{1}\d{1,3}).{1}[a](\d{2}).{1}[q](\d{1,3})"
        #         textfile = open(file, 'r')
        #         matches = []
        #         # reg = re.compile(regex)
        #         for line in textfile:
        #             matches.append(re.match(regex,line))
        #         textfile.close()
        #         newFileName = str(filename_only)+".txt"
        #         lines = []
        #         with open(os.path.join(path_save,newFileName), "w") as myFile:
        #             for match in matches:
        #                 if match is None:
        #                     print(r"Nan,Nan,NaN", file=myFile)
        #                 else:
        #                     new_line = ','.join(match.groups())
        #                     print(new_line, file=myFile)
