# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 21:48:25 2019

@author: scott.downard
"""

#'Stability Reader
#'Input : Directory that points to CSV file generated from Track Image software

import pandas as pd
import numpy as np
import csv
from tkinter import*
from tkinter import filedialog

def getdirectory():
    root = Tk()
    direct = filedialog.askopenfilename(initialdir = "/", title = "Select csv file to read")
    return direct

def trajectory(direct):
    titleflag = False
    headercount = 0
    with open(direct) as f:
        csvfile = csv.reader(f, delimiter = ';')
        for i in csvfile:
            if titleflag == True:
                titlelist = i
                break
            for j in i:            
                if j == 'CHANNELS':
                    titleflag = True
            headercount +=1
    del csvfile
    listcount = 0
    checking = 0
    xlist = [0]
    ylist = [0]
    xlistname = ['Time (msec)']
    ylistname = ['Time (msec)']
    for i in titlelist:
        if 'position.x' in i:
            titlelist[listcount] = 'Time (msec)'
        elif 'position.y' in i:
            titlelist[listcount] = i.replace('_world_position.y','')
        elif i == '':
            titlelist.pop(listcount)
        listcount += 1
    listcount = 0
    for i in titlelist:
        if i[-1] is 'X':
            xlist.append(listcount)
            xlistname.append(i)
        elif i[-1] is 'Y':
            ylist.append(listcount)
            ylistname.append(i)
        listcount += 1
    if len(xlist)==1:
        ydf = pd.read_csv('R&D780B Cushion.csv',names = ylistname, sep = ';', header = headercount, usecols = ylist, index_col = 0)
    elif len(ylist)==1:
        xdf = pd.read_csv('R&D780B Cushion.csv',names = xlistname, sep = ';', header = headercount, usecols = xlist, index_col = 0)
    else:        
        xdf = pd.read_csv('R&D780B Cushion.csv',names = xlistname, sep = ';', header = 5, usecols = xlist, index_col = 0)
        ydf = pd.read_csv('R&D780B Cushion.csv',names = ylistname, sep = ';', header = 5, usecols = ylist, index_col = 0)
    return xdf, ydf
