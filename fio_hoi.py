#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 16:42:45 2019

@author: wang
"""
# =============================================================================
# # attempt 1 with previous examples for reading logfile
# f1 = open('/Users/wang/git/hub/hub/X1.txt', 'r')
# #f2 = open('/Users/wang/git/hub/hub/X2.txt', 'r')
# #f3 = open('/Users/wang/git/hub/hub/X3.txt', 'w')
# 
# y = [1, 2, 3]
# k = 0
# for line in f1:
#     if line[0:66] == '[00:17:41][mapbuildings.cpp:453]: map/buildings.txt error at line ':
# #    if line[0:10] == '[00:17:41]':
# #    if line[0] == '[':
#         print(line[66:71])
# #        y[k] = int(line[66:5])
# #        print('error #', k, ' is in line #', y[k])
# #        k = k + 1     
# f1.close()              
# =============================================================================

# attemp 2 with splitter
# 2.1 read the error file for information
with open('/Users/wang/git/hub/hub/X1.txt', 'r') as infile:
    log = []
    for line in infile:
        if line[0:66] == '[00:17:41][mapbuildings.cpp:453]: map/buildings.txt error at line ':
            tmp = line.split(" ")
            lid, be, was, pv = tmp[5].strip(":"), tmp[17].strip("'"), tmp[22].strip("'"), tmp[26].strip(".")
            log.append([lid, be, was, pv])
L = len(log)
#2.2 read the data file            
outfile = open('/Users/wang/git/hub/hub/X3.txt', 'w+')
with open('/Users/wang/git/hub/hub/X2.txt', 'r') as infile:
    pError = 0  #pointer for error information
    pData = 0   #pointer for data reading line number
    for line in infile:
        pData = pData + 1
        if pData == int(log[pError][0]): #line number equals stored error info
            tmp = line.split(";")
            if tmp[0]==log[pError][1]:  #wrong IDs matches the error info
                tmp[0] = log[pError][2]
            else:
                print('#%d:%d ID %s & %s does not match!' %(pError, pData, tmp[0], log[pError][1]))
                break
            line = " ".join(tmp)
            if pError < L - 1:
                pError = pError + 1
        outfile.write(line)
outfile.close         