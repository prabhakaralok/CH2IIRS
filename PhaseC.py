import numpy as np 
from osgeo import gdal
import gc
import os
import shutil

def Corrector(inPhase, path, outPath):
    print ('its Working')
    inPhase=inPhase+'\\PhaseF'
    
    res=1 # resize factor

    gdal.AllRegister()
    driver=gdal.GetDriverByName('ENVI')
    os.chdir(outPath)

    

    anglePath=path.split('.')[0].split('/')[-1]+'_angle'
    inDSA=gdal.Open(anglePath)



    refPath=path.split('.')[0].split('/')[-1]+'_corrRef'
    inDS=gdal.Open(refPath)


    XSize=inDS.RasterXSize
    YSize=inDS.RasterYSize   

    os.chdir(outPath)
    outN=path.split('.')[0].split('/')[-1]+'_phase'
    outDS=driver.Create(outN,int(XSize*res),int(YSize*res),247,gdal.GDT_Float32)


    for bnd in range(1,248):
        refBND=inDS.GetRasterBand(bnd)
        ref=refBND.ReadAsArray()
        angle=inDSA.ReadAsArray()
        angle[np.where(angle>80)]=80
        #Limb Darkening
        ref=ref*(np.cos(angle*np.pi/180)+1)/np.cos(angle*np.pi/180)
        
        pName=inPhase+'\\'+'fit_'+str(bnd)+'.npy'
        p = np.poly1d(np.load(pName))
        ref=ref*0.46*p(30)/p(angle)        
        
        bd=outDS.GetRasterBand(bnd)
        bd.WriteArray(ref)
    outDS=None

    gc.collect()


    shutil.copy(refPath+'.hdr', outN+'.hdr')