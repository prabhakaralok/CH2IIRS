import numpy as np 
from osgeo import gdal
import os
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET 
from xml.dom import minidom
from scipy.interpolate import interp1d



def Incidence(inSolar, path, outPath):


    gdal.AllRegister()
    driver=gdal.GetDriverByName('ENVI')

    xmlPath='/'.join(path.split('.')[:-1])+'.xml'
    spmPath='/'.join(path.split('/')[:-4])+'/miscellaneous/calibrated/'+path.split('/')[-2]+'/'+path.split('/')[-1].split('.')[0]+'.spm'

    res=1 # resize factor

    path1=path 
    inDS=gdal.Open(path1)
    XSize=inDS.RasterXSize
    YSize=inDS.RasterYSize

    ### Get inclination

    mydoc = minidom.parse(xmlPath)
    start_time_String = mydoc.getElementsByTagName('start_date_time')[0].firstChild.data
    start_time=datetime.strptime(start_time_String,'%Y-%m-%dT%H:%M:%S.%fZ').timestamp()
    incImage = np.zeros((YSize,XSize))
    phaseImage = np.zeros((YSize,XSize))
    timeArr = np.zeros((YSize))

    tm=[]
    ang=[]
    phas=[]
    with open(spmPath) as inp:
        for line in inp:
            sp=line.strip().split()
            angle=abs(float(sp[-1]))
            phase=abs(float(sp[-4]))
            yr=sp[2][3:]
            time=[yr]+sp[3:9]
            time=datetime.strptime(str(time),"['%Y', '%m', '%d', '%H', '%M', '%S', '%f']").timestamp()
            tm.append(time)
            ang.append(angle)
    outAngle=interp1d(tm,ang,kind='linear')

    for i in range(YSize):
        sc_time=start_time+0.05306*(i)
        timeArr[i]=sc_time
        try:
            incImage[i,:]=90-outAngle(sc_time)
        except:
            incImage[i,:]=0
            print('mismatch in xml and spm')
        

    os.chdir(outPath)
    outN=path.split('.')[0].split('/')[-1]+'_angle'
    outDST=driver.Create(outN,XSize,YSize,1,gdal.GDT_Float32)
    bnd=outDST.GetRasterBand(1)
    bnd.WriteArray(incImage)
    outDST=None