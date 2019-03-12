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
import xlsxwriter
import openpyxl
from bokeh.plotting import figure
from bokeh.io import push_notebook, show, output_notebook
from bokeh.models import ColumnDataSource
output_notebook()


def getdirectory():
    root = Tk()
    direct = filedialog.askopenfilename(initialdir = "/", title = "Select csv file to read")
    root.destroy()
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
        ydf = pd.read_csv(direct,names = ylistname, sep = ';', header = headercount, usecols = ylist, index_col = 0)
        return ydf
    elif len(ylist)==1:
        xdf = pd.read_csv(direct,names = xlistname, sep = ';', header = headercount, usecols = xlist, index_col = 0)
        return xdf
    else:        
        xdf = pd.read_csv(direct,names = xlistname, sep = ';', header = 5, usecols = xlist, index_col = 0)
        ydf = pd.read_csv(direct,names = ylistname, sep = ';', header = 5, usecols = ylist, index_col = 0)
        return xdf, ydf
#Function is used to append data frame from TrackImage data into a Master Excel sheet.
def excelReport(buildsheet,xdf,ydf):
    result = pd.concat([xdf,ydf],sort = False, axis=1)
    with pd.ExcelWriter('StabilityMaster.xlsx',mode = 'a',engine='openpyxl') as writer:
        result.to_excel(writer,sheet_name=buildsheet)


def analyze(df):
    plot = figure()
    src = ColumnDataSource(df)
    srcdict = dict(src.data)
    keylist = list(srcdict.keys())
    plot.line(source = src,x = keylist[0], y = [i for i in keylist[1:]])
    show(plot)



