#Written by Siddarth Sreeram
#Background information/data acquired from:
#https://www.kaggle.com/datasets/mbogernetto/brazilian-amazon-rainforest-degradation?select=inpe_brazilian_amazon_fires_1999_2019.csv
#https://www.kaggle.com/datasets/programmerrdai/co2-levels-globally-from-fossil-fuels

# import necessary packages
from turtle import bgcolor
import matplotlib
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd
from matplotlib import cm
from sklearn.metrics import r2_score
import scipy as spi
from cProfile import label
from ctypes import Structure
from matplotlib import cm
from sklearn.metrics import r2_score
import scipy as spi
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGraphicsView, QLabel, QPlainTextEdit, QPushButton, QTextBrowser
from PyQt5 import uic
import sys
import seaborn as sn
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt

#use pandas to read CSV data - **Adjust to location of CSV on one's computer**

df = pd.read_csv('inpe_brazilian_amazon_fires_1999_2019.csv')

lon = []
lat = []
colorslist = []
for i in range(0, len(df)):
    lon.append(df._get_value(i, 'longitude'))
    lat.append(df._get_value(i, 'latitude'))
    colorslist.append((df._get_value(i, 'firespots')))

df2=pd.read_csv("global.csv")
df3=pd.read_csv("def_area_2004_2019.csv")

CO2List1=[]
TotalFiresList1=[]
for i in range(253, 260):
    CO2List1.append(df2._get_value(i,'Total'))
for i in range(0, 7):
    TotalFiresList1.append(df3._get_value(i,'AMZ LEGAL'))

#main PyQt5 window
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #Load the UI file
        uic.loadUi("CO2GUI.ui", self)

        #define widgets
        self.label = self.findChild(QLabel, "label")
        self.backgroundTxt = self.findChild(QTextBrowser, "textBrowser")
        self.button1 = self.findChild(QPushButton, "pushButton")
        self.button2 = self.findChild(QPushButton, "pushButton_2")
        self.button3 = self.findChild(QPushButton, "pushButton_3")

        #button works
        self.button1.clicked.connect(self.heatmap)
        self.button2.clicked.connect(self.states)
        self.button3.clicked.connect(self.CO2)

        #show app
        self.setStyleSheet("background-color: navajowhite;")
        self.show()
    def heatmap(self):
        with plt.style.context('Solarize_Light2'):
            plt.figure()
            m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=15,\
                        llcrnrlon=-90,urcrnrlon=-30,lat_ts=20,resolution='c')
            m.etopo()
            m.drawcountries()

            lons, lats = m(lon, lat)
            m.scatter(lons, lats, marker = 'x', c=colorslist, cmap=cm.gist_heat, zorder=5, norm=matplotlib.colors.LogNorm())
            listMax=max(colorslist)
            listMin=min(colorslist)
            plt.clim(listMin, listMax)
            plt.title("Fire Outbreaks in the Brazilian Amazon between 1990 and 2019")
            plt.colorbar(label="Amount of Firespots", orientation="horizontal")
            plt.figtext(0.35, 0.01, "*Each 'x' represents the average position of a fire in a certain state per month \ncolor represents the number of fires per month")
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            plt.show(block=False)
    def states(self):
        with plt.style.context('Solarize_Light2'):
            plt.figure()
            plt.plot(df3["Ano/Estados"], df3["AMZ LEGAL"], label="Total $km^2$ of Brazilian Amazon burned")
            plt.plot(df3["Ano/Estados"], df3["AC"], label="$km^2$ of Brazilian Amazon burned in AC state")
            plt.plot(df3["Ano/Estados"], df3["AM"], label="$km^2$ of Brazilian Amazon burned in AM state")
            plt.plot(df3["Ano/Estados"], df3["AP"], label="$km^2$ of Brazilian Amazon burned in AP state")
            plt.plot(df3["Ano/Estados"], df3["MA"], label="$km^2$ of Brazilian Amazon burned in MA state")
            plt.plot(df3["Ano/Estados"], df3["MT"], label="$km^2$ of Brazilian Amazon burned in MT state")
            plt.plot(df3["Ano/Estados"], df3["PA"], label="$km^2$ of Brazilian Amazon burned in PA state")
            plt.plot(df3["Ano/Estados"], df3["RO"], label="$km^2$ of Brazilian Amazon burned in RO state")
            plt.plot(df3["Ano/Estados"], df3["RR"], label="$km^2$ of Brazilian Amazon burned in RR state")
            plt.plot(df3["Ano/Estados"], df3["TO"], label="$km^2$ of Brazilian Amazon burned in TO state")
            plt.legend(loc="upper right")
            plt.xlabel("Year")
            plt.ylabel("$km^2$ of Brazilian Rainforest Burned")
            plt.title("$km^2$ of Brazilian Rainforest Burned \n in Various States between 2004 and 2019")
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            plt.show(block=False)
    def CO2(self):
        with plt.style.context('Solarize_Light2'):
            plt.figure()
            plt.title("Number of Forest Fires Within the Brazilian Amazon \n between 2004 and 2010")
            combinedList=[]
            for i in range(0,7):
                combinedList.append(float(CO2List1[i])/TotalFiresList1[i])
            combinedList2=np.array(combinedList)
            yearList=[2004, 2005, 2006, 2007, 2008, 2009, 2010]
            yearList2=np.array(yearList)
            plt.scatter(yearList, combinedList, color='red')
            a, b = np.polyfit(yearList2, combinedList2, 1)
            plt.plot(yearList2, a*yearList2+b, color='purple', linestyle='--', linewidth=2)
            slope, intercept, r_value, p_value, std_err = spi.stats.linregress(yearList2, combinedList2)
            plt.text(2008, 1.266, 'y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x' + "\n $R^2$="+str(float(r_value)**2), size=14)
            plt.xlabel("Year")
            plt.ylabel("Ratio between Global $CO_2$ Concentration and \n Brazilian Forest Fires")
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            plt.show(block=False)


#initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()