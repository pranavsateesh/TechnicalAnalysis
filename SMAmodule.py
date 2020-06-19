import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def dataread(path):
    data = pd.read_csv(path)
    data = data.dropna(axis=0)
    data = data.reset_index(drop=True)
    return data
def datacondition(path,Startdate,Enddate):
    data = dataread(path)
    data.date = pd.to_datetime(data.Date)
    sets = (data.date >= Startdate) & (data.date <= Enddate)
    dataclose = data.Close.loc[sets].reset_index(drop=True)
    datadate = data.Date.loc[sets].reset_index(drop=True)
    return dataclose, datadate

def signalout(path,Startdate,Enddate,short,long):
    dataclose,datadate = datacondition(path,Startdate,Enddate)
    print(dataclose,datadate)
    signal = pd.DataFrame(index = dataclose.index)
    signal['meanshort']= dataclose.rolling(window=short).mean()
    signal['meanlong'] = dataclose.rolling(window=long).mean()
    signal['signal']= (np.where(signal['meanshort'] > signal['meanlong'], 1.0, 0.0)) 
    signal['position'] = signal['signal'].diff()
    plt.plot(signal.loc[signal.position == 1.0].index,signal.meanshort[signal.position == 1.0],'^', markersize=10, color='m')
    plt.plot(signal.loc[signal.position == -1.0].index,signal.meanlong[signal.position == -1.0],'v', markersize=10, color='k')
    signal['meanshort'].plot()
    signal['meanlong'].plot()
    plt.plot(datadate,dataclose)
    plt.legend(['Buy indicator','Sell indicator','MA :%d'%short,'MA :%d'%long,'Close'])
    plt.xlabel('Dates')
    plt.ylabel('Close Price')
    plt.show()


