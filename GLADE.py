from astroquery.simbad import Simbad
from astroquery.vizier import VizierClass
from astropy.coordinates import SkyCoord
import pandas as pd
import astropy.units as u
import numpy as np
import requests 
import boto3
import io
import fsspec

def GLADEV2coordinates():

    fn = fsspec.open_local(f'simplecache::s3://gxgwtest/GLADE.h5')
    data = pd.read_hdf(fn, 'df')  
   
    data.columns=['PGC','GWGC','HyperLEDA','2MASS','SDSS','flag1','RA','Dec','dist','dist_err','z','Bmag','e_Bmag','AbsBMag','Jmag','e_Jmag','Hmag','e_Hmag','Kmag','eKmag','flag2','flag3']

    # msk3=data[['dist']]>0
    # msk4=data[['dist']]!="NaN"
    # msk5=data[['Bmag']]!="NaN" 
    # msk6=data[['Bmag']]!="null"
    # msk7=data[['Bmag']]>0 
    # msk=pd.concat((msk3,msk4,msk5,msk6,msk7),axis=1)
    # slct=msk.all(axis=1)
    # data=data.loc[slct]
    print('lengthofdata',len(data))
    data['source']='GLADE'
    
    coordinates=SkyCoord(data['RA'].values*u.deg, data['Dec'].values*u.deg)
    
    return coordinates,data


def PS1coordinates(filename):

    data = pd.read_csv(filename)


    #data=pd.read_csv('GW190924h_1_Lana_S.csv',usecols=['RA','Dec','rMeanKronMag'])
    #data=pd.read_csv('PS1.csv',usecols=['raMean','decMean','rMeanKronMag'])
    #previously
    #data=pd.read_csv('GW191213g_1_Lana_S.csv',usecols=['RA','Dec','rMeanKronMag'])
    #new 191213g
    #data=pd.read_csv('GW191213g_total1_Lana_S.csv',usecols=['RA','Dec','rMeanKronMag'])
    #    data=pd.read_csv(filename,usecols=['RA','Dec','rMeanKronMag'])
    #data=pd.read_csv('GW200129m_total1_Lana_S.csv',usecols=['RA','Dec','rMeanKronMag'])
    

    msk5=data[['rMeanKronMag']]<=19.5
    msk6=data[['rMeanKronMag']]>=14
    #msk7=data[['Bmag']]>0 
    msk=pd.concat((msk5,msk6),axis=1)
    slct=msk.all(axis=1)
    data=data.loc[slct]
    data['source']='PS1'

    coordinates=SkyCoord(data['RA'].values*u.deg, data['Dec'].values*u.deg)
    return coordinates,data

